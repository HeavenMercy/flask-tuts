from flask import Blueprint, request, jsonify

from werkzeug.security import generate_password_hash
from uuid import uuid4

from .. import db
from ..models import User
from .auth import token_required, admin_required

_ = Blueprint('user', __name__, url_prefix='/user')

@_.route('', methods=['GET'])
@token_required
def get_all_users(_):
    try:
        return jsonify([{
            'hash': user.hash,
            'name': user.uname
        } for user in User.query.all()])
    except: return jsonify({'message': 'failed to get all users'}), 500

@_.route('/<hash>', methods=['GET'])
@token_required
def get_one_user(current_user, hash):
    if current_user.hash != hash:
        no_admin_resp = admin_required(current_user)
        if no_admin_resp: return no_admin_resp

    try:
        user = User.query.filter(User.hash == hash).first()

        return jsonify({
            'hash': user.hash,
            'name': user.uname,
            'admin': user.admin,
            'creation_date': user.creation_date
        })
    except: return jsonify({"message": f"failed to get user with hash '{hash}'"}), 500

@_.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    UNAME_KEY = 'username'
    PASSWD_KEY = 'password'

    if UNAME_KEY not in data: return jsonify({ "message": f"missing key '{UNAME_KEY}'" })
    if PASSWD_KEY not in data: return jsonify({ "message": f"missing key '{PASSWD_KEY}'" })

    name = data[UNAME_KEY]
    hashed_passwd = generate_password_hash(data[PASSWD_KEY])

    try:
        hash=str(uuid4())

        user = User(hash=hash, uname=name, passwd=hashed_passwd, admin=False)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "user successfully created",
            "user_hash": hash
        }), 201
    except: return jsonify({ "message": f"failed to add the user '{name}' (seems like he already exists)" })

@_.route('/<hash>', methods=['PUT'])
@token_required
def promote_user(current_user, hash):
    no_admin_resp = admin_required(current_user)
    if no_admin_resp: return no_admin_resp

    try:
        user = User.query.filter(User.hash == hash).first()

        user.admin = True
        db.session.commit()

        return jsonify({ "message": f"promotion of user '{user.uname}' successfully done" })
    except: return jsonify({"message": f"failed to promote user with hash '{hash}'"}), 500

@_.route('/<hash>', methods=['DELETE'])
@token_required
def delete_user(current_user, hash):
    no_admin_resp = admin_required(current_user)
    if no_admin_resp: return no_admin_resp

    try:
        user = User.query.filter(User.hash == hash).first()

        db.session.delete(user)
        db.session.commit()

        return jsonify({ "message": f"deletion of user '{user.uname}' successfully done" })
    except: return jsonify({"message": f"failed to delete user with hash '{hash}'"}), 500
