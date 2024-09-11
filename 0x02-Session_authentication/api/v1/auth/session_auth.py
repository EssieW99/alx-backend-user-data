#!/usr/bin/env python3
""" Basic Auth"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User
import os


class SessionAuth(Auth):
    """
    session authentication mechanism
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a new instance providing a session id
        """

        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())

        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """

        if session_id is None or type(session_id) is not str:
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
         returns a User instance based on a cookie value
        """

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)

        return user
