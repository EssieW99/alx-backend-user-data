#!/usr/bin/env python3
""" Flask application"""

from auth import Auth
from db import DB
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """ index page"""

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """
    an endpoint that registers a new user
    """

    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({f'"email": email, "message": "user created"'}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
