#!/usr/bin/env python3
""" Authentication file"""

from user import User
from db import DB
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound


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

        try:
            user = db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        credential validation
        """

        db = self._db

        try:
            user = db.find_user_by(email=email)
            passwd = password.encode('utf-8')
            return bcrypt.checkpw(passwd, user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email, generate a new UUID and
        store it in the database as the user’s session_id,
        then return the session ID
        """

        db = self._db

        try:
            user = db.find_user_by(email=email)
            session_id = _generate_uuid()
            db.update_user(user.id, session_id=session_id)
            return user.session_id
        except (NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        finds a user by the session id
        """

        db = self._db

        if session_id is None:
            return None

        try:
            user = db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, ValueError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates the user's session ID to None
        """
        db = self._db

        if user_id is None:
            return None
        try:
            db.update_user(user_id=user_id, session_id=None)
            return None
        except (NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a reset password token
        """

        db = self._db

        try:
            user = db.find_user_by(email=email)
            reset_token = _generate_uuid()
            db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError
