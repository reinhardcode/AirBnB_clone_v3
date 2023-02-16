#!/usr/bin/python3
"""review view"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, make_response, request
from os import getenv


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """get the list of reviews of a place based on id"""
    place = storage.get(Place, place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            reviews = place.reviews
        else:
            reviews = place.reviews()
        lst_r = [review.to_dict() for review in reviews]
        return jsonify(lst_r), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """get review with the given id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """delete review with given id"""
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """create review for a given city id"""
    place = storage.get(Place, place_id)
    if place:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if 'user_id' not in request.json:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        user = storage.get(User, request.json['user_id'])
        if not user:
            return make_response(jsonify({"error": "Not found"}), 404)
        if 'text' not in request.json:
            return make_response(jsonify({"error": "Missing text"}), 400)
        review_dict = request.json
        review_dict.update({'place_id': place_id})
        new_review = Review(**review_dict)

        new_review.save()
        return jsonify(new_review.to_dict()), 201
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """updates review based on the review_id"""
    review = storage.get(Review, review_id)
    if review:
        if not request.json:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        data = request.json
        data = {k: v for k, v in data.items() if k != 'id' and
                k != 'created_at' and k != 'updated_at'}
        for k, v in data.items():
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)
