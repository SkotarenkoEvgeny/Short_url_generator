from datetime import datetime

from src import db


class ScortUrl(db.Model):
    __tablename__ = 'short_urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False, unique=True)
    short_url = db.Column(db.String(8), nullable=False, unique=True)
    last_time = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        if datetime.today() > self.last_time:
            time = self.last_time.date()
        else:
            time = 'expected'
        return f'Url-{self.id}-{self.short_url}-{time}'
