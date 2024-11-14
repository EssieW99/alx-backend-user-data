#!/usr/bin/env python3
""" session authentication"""

from api.v1.views import app_views
from flask import Flask, request, jsonify, make_response
from models.user import User
from models.base import Base
from api.v1.auth.session_auth import SessionAuth
import os


app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
    authentication based on a Session ID stored in a cookie
    """

    email = request.form.get('email')
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user_id = user.id

    auth_instance = SessionAuth()
    session_id = auth_instance.create_session(user_id)
    session_name = os.getenv('SESSION_NAME')

    user_data = user.to_json()

    response = make_response(jsonify(user_data))
    response.set_cookie(session_name, session_id)
    return response
