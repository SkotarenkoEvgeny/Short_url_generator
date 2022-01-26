from datetime import datetime, timedelta

from flask import redirect, request
from flask_restful import Resource
from marshmallow import ValidationError

from src import api, db
from src.models import ScortUrl
from src.schemas import SchortUrlSchema
from src.workers import generate_short_id, short_url_complexity


class ShortUrlApi(Resource):
    short_url_schema = SchortUrlSchema()

    def get(self, short_url=None):
        """
        file: swagger/short_url_get.yml
        """
        if not short_url:
            return {'message': 'url not passed'}, 400
        url = db.session.query(ScortUrl).filter_by(short_url=short_url).first()
        if url:
            if url.last_time >= datetime.today():
                return redirect(url.original_url), 301
            else:
                return {'message': f'The url {url.short_url} time was out'}, 400
        else:
            return {'message': 'Short url not found'}, 404

    def post(self):
        """
        file: swagger/short_url_post.yml
        """
        url_json = request.json
        if not url_json:
            return {'message': 'Wrong data'}, 400
        try:
            data_url_list = {i.original_url: (i.short_url, i.last_time) for i
                             in db.session.query(ScortUrl).all()}
            raw_value = data_url_list.get(url_json['original_url'], None)
            # chek existing urls
            if raw_value:
                if raw_value[1] < datetime.today():
                    return {'message': 'url out of data'}, 400
                return {
                    'short_url': request.host_url + raw_value[0],
                    'last_time': raw_value[1].isoformat()
                    }
            # generate short url
            while raw_value is None or raw_value in [i[0] for i in
                                                     data_url_list.values()]:
                url_length = short_url_complexity(len(data_url_list))
                raw_value = generate_short_id(url_length)
            url_json["short_url"] = raw_value
            # generate working days
            days_value = str(url_json.get('last_time', None))
            days = 90
            if days_value:
                if days_value.isdigit():
                    days = int(days_value)
                    if days > 365:
                        days = 365
            temp_days = datetime.today() + timedelta(days=int(days))
            url_json['last_time'] = temp_days.isoformat()

            url = self.short_url_schema.load(url_json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(url)
        db.session.commit()
        raw_data_url = request.host_url + url['short_url']
        url['short_url'] = raw_data_url
        return self.short_url_schema.dump(url), 201

    def delete(self, short_url=None):
        """
        file: swagger/short_url_del.yml
        """
        if not short_url:
            return {'message': 'url not passed'}, 400
        url = db.session.query(ScortUrl).filter_by(short_url=short_url).first()
        db.session.delete(url)
        db.session.commit()
        return {'message': f'{short_url} - deleted'}, 201


api.add_resource(ShortUrlApi, '/', '/<short_url>', strict_slashes=False)
