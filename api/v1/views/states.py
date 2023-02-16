#!/usr/bin/python3
"""states view"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, make_response, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """retrieve the list of all state obj"""
    states = storage.all(State)

    lst = [state.to_dict() for state in states.values()]

    return jsonify(lst)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id=""):
    """retrieve a particular state based on its id"""
    if state_id != "":
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=""):
    """deletes the state specified by the id"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """create a new state"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(name=request.json['name'])
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """updates a state"""
    if request.is_json:
        state = storage.get(State, state_id)
        if state is not None:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at'}
            for k, v in data.items():
                setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200
        return make_response(jsonify({"error": "Not found"}), 404)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
