from . import db

from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hash = db.Column(db.String(50), unique=True)
    uname = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(80), nullable=False)

    admin = db.Column(db.Boolean)
    creation_date = db.Column(db.Date, default=date.today())

    def __repr__(self) -> str:
        return f'<User {self.id}>'