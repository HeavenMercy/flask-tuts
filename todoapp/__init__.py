from flask import Flask
from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'thisisasupersecretkey'

db.init_app(app)
app.app_context().push()

def rebuild_db():
    db.drop_all()
    db.create_all()

from .modules import auth, user, todo
