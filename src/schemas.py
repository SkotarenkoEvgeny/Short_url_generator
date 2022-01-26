from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models import ScortUrl


class SchortUrlSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ScortUrl
        exclude = ['id']
        load_instance = True
