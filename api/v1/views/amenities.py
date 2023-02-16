#!/usr/bin/python3
"""amenities view"""
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, make_response, request
from os import getenv


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def get_amenities():
    """return the list of amenities in json"""
    amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in amenities.values()]

    return jsonify(amenities), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """get amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/amenities',
                 strict_slashes=False, methods=['POST'])
def create_amenity():
    """create new amenity"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(name=request.json['name'])
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """updates amenity based on the amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.json
        data = {k: v for k, v in data.items() if k != 'id' and
                k != 'created_at' and k != 'updated_at'}
        for k, v in data.items():
            setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
