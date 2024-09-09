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
        returns True if the path is not in the list of strings excluded_paths
        """

        if path is None:
            return True

        """ ensure path ends with a '/' """
        norm_path = path if path.endswith('/') else path + '/'

        if not excluded_paths:
            return True

        return norm_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        checks if a flask request has an authorization header
        """

        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        checks the current user of a flask request
        """

        return None
