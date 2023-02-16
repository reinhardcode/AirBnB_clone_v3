#!/usr/bin/python3
"""places view"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request
from os import getenv


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """get places for a city id"""
    city = storage.get(City, city_id)
    if city:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            places = city.places
        else:
            places = city.places()
        lst_p = [place.to_dict() for place in places]
        return jsonify(lst_p), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """get place with the given id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """delete place with given id"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """create place for a given city id"""
    city = storage.get(City, city_id)
    if city:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if 'user_id' not in request.json:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        user = storage.get(User, request.json['user_id'])
        if not user:
            return make_response(jsonify({"error": "Not found"}), 404)
        if 'name' not in request.json:
            return make_response(jsonify({"error": "Missing name"}), 400)
        place_dict = request.json
        place_dict.update({'city_id': city_id})
        new_place = Place(**place_dict)

        new_place.save()
        return jsonify(new_place.to_dict()), 201
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """updates place based on the place_id"""
    place = storage.get(Place, place_id)
    if place:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.json
        data = {k: v for k, v in data.items() if k != 'id' and
                k != 'created_at' and k != 'updated_at'}
        for k, v in data.items():
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
