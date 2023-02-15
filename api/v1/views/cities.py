#!/usr/bin/python3
"""cities view"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, make_response, request
from os import getenv


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_state_cites(state_id):
    """get the cities for a given state based on state_id
    """
    state = storage.get(State, state_id)
    if state:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            cities = state.cities
        else:
            cities = state.cities()
        lst_c = [city.to_dict() for city in cities]
        return jsonify(lst_c), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """get city with the given id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete city with given id"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """create city for a given state id"""
    state = storage.get(State, state_id)
    if state:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if 'name' not in request.json:
            return make_response(jsonify({"error": "Missing name"}), 400)
        city_dict = request.json
        city_dict.update({'state_id': state_id})
        new_city = City(**city_dict)

        new_city.save()
        return jsonify(new_city.to_dict()), 201
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """updates city based on the city id"""
    city = storage.get(City, city_id)
    if city:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.json
        data = {k: v for k, v in data.items() if k != 'id' and
                k != 'created_at' and k != 'updated_at'}
        for k, v in data.items():
            setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
