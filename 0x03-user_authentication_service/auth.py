#!/usr/bin/env python3
""" Authentication file"""

from user import User
from db import DB
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password
    """

    """ convert password to array of bytes"""
    bytes = password.encode('utf-8')

    """ generate the salt"""
    salt = bcrypt.gensalt()

    """ hashing the password"""
    hashed_passwd = bcrypt.hashpw(bytes, salt)

    return hashed_passwd


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """

    id = str(uuid.uuid4())

    return id


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        credential validation
        """

        db = self._db
        user = db.find_user_by(email=email)

        if user:
            try:
                passwd = password.encode('utf-8')
                return bcrypt.checkpw(passwd, user.hashed_password)

            except Exception:
                return False
        else:
            return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email, generate a new UUID and
        store it in the database as the user’s session_id,
        then return the session ID
        """

        db = self._db

        user = db.find_user_by(email=email)

        if user:
            session_id = _generate_uuid()
            db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        finds a user by the session id
        """

        db = self._db

        if session_id is None:
            return None

        user = db.find_user_by(session_id=session_id)

        if not user:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """
        destroys a session and updates the user's session id to None
        """
        pass
