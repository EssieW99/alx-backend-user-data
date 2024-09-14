#!/usr/bin/env python3
""" Authentication file"""

from user import User
from db import DB
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    salt hashes the inputed password with bcrypt.hashpw
    """

    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a user
        """

        db = self._db

        user = db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {user.email} already exists")

        hashed_password = _hash_password(password)
        db.add_user(email, hashed_password)
