#!/usr/bin/env python3
""" Auth class"""

from flask import request
from typing import List, TypeVar, Generic


class Auth:
    """
    class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if a path requires authentication and returns True or False
        """

        return False

    def authorization_header(self, request=None) -> str:
        """
        checks if a flask request has an authorization header
        """

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks the current user of a flask request
        """

        return None
