from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Todo
from app import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash

auth_routes = Blueprint('auth', __name__)
todo_routes = Blueprint('todos', __name__)

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@todo_routes.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_todo = Todo(
        title=data.get('title'),
        description=data.get('description'),
        user_id=user_id
    )
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"message": "Todo created successfully"}), 201

@todo_routes.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": todo.id, "title": todo.title, "description": todo.description} for todo in todos]), 200

@todo_routes.route('/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({"message": "Todo not found"}), 404

    if request.method == 'PUT':
        data = request.get_json()
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        db.session.commit()
        return jsonify({"message": "Todo updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully"}), 200