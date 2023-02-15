#!/usr/bin/python3
"""states view"""

from api.v1.views import app_views
from flask import jsonify, make_response, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """retrieve the list of all state obj"""
    from models import storage
    from models.state import State

    states = storage.all(State)

    lst = [state.to_dict() for state in states.values()]

    return jsonify(lst)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id=""):
    """retrieve a particular state based on its id"""
    if state_id != "":
        from models import storage
        from models.state import State

        states = storage.all(State)
        id = state_id

        lst = [state.to_dict() for state in states.values() if state.id == id]
        if lst != []:
            return jsonify(lst[0])
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=""):
    """deletes the state specified by the id"""
    from models import storage
    from models.state import State

    id = state_id
    states = storage.all(State)
    lst = [state for state in states.values() if state.id == id]
    if lst != []:
        lst[0].delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """create a new state"""
    from models import storage
    from models.state import State

    if not request.json:
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')

    new_state = State(name=request.json['name'])
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """updates a state"""
    from models import storage
    from models.state import State
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
        abort(404)
    abort(400, description='Not a JSON')
