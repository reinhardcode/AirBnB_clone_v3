#!/usr/bin/python3
"""cities view"""
from models import storage
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request
from os import getenv


@app_views.route('/users',
                 strict_slashes=False, methods=['GET'])
def get_users():
    """return all users"""
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]

    return jsonify(users), 200


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """get user based on id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """delete user by user_id"""
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users',
                 strict_slashes=False, methods=['POST'])
def create_user():
    """create new user"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({"error": "Missing password"}), 400)

    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """updates user based on the user_id"""
    user = storage.get(User, user_id)
    if user:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.json
        data = {k: v for k, v in data.items() if k != 'id' and
                k != 'created_at' and k != 'updated_at'}
        for k, v in data.items():
            setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
