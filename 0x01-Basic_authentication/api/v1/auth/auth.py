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
        norm_path = path if path.endswith(('/', '*')) else path + '/'

        if not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if norm_path.startswith(excluded_path[:-1]):
                    return False

        return norm_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        checks whether a flask request has an authorization header key
        """

        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        checks the current user of a flask request
        """

        return None
