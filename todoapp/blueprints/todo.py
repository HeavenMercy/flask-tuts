from flask import Blueprint, jsonify, request
from uuid import uuid4

from .. import db

from ..models import Todo, User

from .auth import token_required, admin_required

_ = Blueprint('todo', __name__, url_prefix='/todo')

@_.route('', methods=['GET'])
@token_required
def get_all_todos(current_user):
    try:
        todos = Todo.query.filter(Todo.user_id == current_user.id).all()

        return jsonify([{
            'hash': todo.hash,
            'title': todo.title
        } for todo in todos])
    except: return jsonify({"message": f"failed to get all todos for user with hash '{hash}'"}), 500

@_.route('/all', methods=['GET'])
@token_required
def admin_get_all_todos(current_user):
    no_admin_resp = admin_required(current_user)
    if no_admin_resp: return no_admin_resp

    try:
        todos = Todo.query.all()

        return jsonify([{
            'hash': todo.hash,
            'title': todo.title,
            'user_hash': User.query.filter(User.id == todo.user_id).first().hash
        } for todo in todos])
    except: return jsonify({"message": f"failed to get all todos for user with hash '{hash}'"}), 500


@_.route('/<hash>', methods=['GET'])
@token_required
def get_todo(current_user, hash):
    try:
        todo = Todo.query.filter(Todo.user_id == current_user.id, Todo.hash == hash).first()

        return jsonify({
            'hash': todo.hash,
            'title': todo.title,
            'completed': todo.completed,
            'creation_date': todo.creation_date
        })
    except: return jsonify({"message": f"failed to get todo with hash '{hash}'"}), 500

@_.route('', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()
    TITLE_KEY = 'title'

    if TITLE_KEY not in data: return jsonify({ "message": f"missing key '{TITLE_KEY}'" })

    title = data[TITLE_KEY]
    try:
        hash = str(uuid4())
        todo = Todo(hash=hash, title=title, completed=False, user_id=current_user.id)

        db.session.add(todo)
        db.session.commit()

        return jsonify({
            "message": "todo successfully created",
            "todo_hash": hash
        }), 201
    except: return jsonify({ "message": f"failed to create todo '{title}' for the user" })

@_.route('/<hash>', methods=['PUT'])
@token_required
def complete_todo(current_user, hash):
    try:
        todo = Todo.query.filter(Todo.user_id == current_user.id, Todo.hash == hash).first()

        todo.completed = True
        db.session.commit()

        return jsonify({"message": f"todo completed successfully"})
    except: return jsonify({"message": f"failed to complete todo with hash '{hash}'"}), 500

@_.route('/<hash>', methods=['DELETE'])
@token_required
def delete_todo(current_user, hash):
    try:
        todo = Todo.query.filter(Todo.user_id == current_user.id, Todo.hash == hash).first()

        db.session.delete(todo)
        db.session.commit()

        return jsonify({"message": f"todo deleted successfully"})
    except: return jsonify({"message": f"failed to delete todo with hash '{hash}'"}), 500


