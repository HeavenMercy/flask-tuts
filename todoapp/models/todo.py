from . import db

from datetime import date

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hash = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean)
    creation_date = db.Column(db.Date, default=date.today())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Todo {self.id}>'