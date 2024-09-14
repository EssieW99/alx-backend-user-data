#!/usr/bin/env python3
""" Flask application"""

from db import DB
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)


@app.route('/')
def index():
    """ index page"""

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
