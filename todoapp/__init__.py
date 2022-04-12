from flask import Flask
from .models import db

from .blueprints import auth, user, todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(auth._)
app.register_blueprint(user._)
app.register_blueprint(todo._)

db.init_app(app)
app.app_context().push()

def rebuild_db():
    db.drop_all()
    db.create_all()

