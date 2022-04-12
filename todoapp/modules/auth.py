from flask import request, jsonify, make_response

from werkzeug.security import check_password_hash

from functools import wraps
import jwt, datetime

from .. import app
from ..models import User

SECRET = app.config['SECRET_KEY']

TOKEN_KEY_HASH = 'hash'

@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization

    if not auth \
    or not auth.username \
    or not auth.password:
        return make_response(
            jsonify({'message':'could not verify authentication'}), 401,
            {'WWW-Authenticate': 'Basic realm="login required!"'} )

    user = User.query.filter(User.uname == auth.username).first()
    if not user \
    or check_password_hash(auth.password, user.passwd):
        return jsonify({'message':'wrong credentials received'}), 401

    token = jwt.encode({
        TOKEN_KEY_HASH: user.hash,

        'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
    }, SECRET, algorithm='HS256')

    return jsonify({
        'message': 'user successfully authenticated',
        'token': token
    })

def token_required(route_method):
    """specifies that the decorated route require a `X-auth-token` header to be executed

    Args:
        route_method (_type_): the route requiring a token
    """
    @wraps(route_method)
    def _(*args, **kwargs):
        token = request.headers.get('X-auth-token', None)

        if token:
            try:
                payload = jwt.decode(token, SECRET, algorithms=['HS256'])

                now = int(round(datetime.datetime.now().timestamp(), 0))
                if now > payload['exp']: raise Exception

                current_user = User.query.filter(User.hash == payload[TOKEN_KEY_HASH]).first()
                return route_method(current_user, *args, **kwargs)
            except: pass

        return jsonify({'message': 'access denied (no, wrong or expired token submitted)'}), 401

    return _


def admin_required(user: User):
    if not user.admin:
        return jsonify({ 'message': 'operation not permitted (you must be an admin)' })