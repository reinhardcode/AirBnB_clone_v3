#!/usr/bin/python3
"""update this comment"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns the stats, number of objs"""
    stats_dic = {}
    from models import storage

    from models.state import State
    from models.amenity import Amenity
    from models.city import City
    from models.user import User
    from models.review import Review
    from models.place import Place
    
    stats_dic.update({"amenities": storage.count(Amenity)})
    stats_dic.update({"cities": storage.count(City)})
    stats_dic.update({"places": storage.count(Place)})
    stats_dic.update({"reviews": storage.count(Review)})
    stats_dic.update({"states": storage.count(State)})
    stats_dic.update({"users": storage.count(User)})

    return jsonify(stats_dic)

