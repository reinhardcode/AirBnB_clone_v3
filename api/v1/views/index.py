#!/usr/bin/python3
"""update this comment"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', , strict_slashes=False)
def status():
    """blueprint function"""
    return jsonify({"status": "OK"})
