#!/usr/bin/env python3
""" Basic Auth"""

from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header for a Basic Auth
        """

        if authorization_header is None or type(authorization_header) != str:
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
         returns the decoded value of a Base64 string
         base64_authorization_header
        """

        base64_header = base64_authorization_header
        if base64_header is None or type(base64_header) != str:
            return None

        try:
            base64_header + '=' * ((4 - len(base64_header) % 4) % 4)

            return base64.b64decode(base64_header).decode('utf-8')

        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):   # type: ignore

        """
        returns the user email and password from the Base64 decoded value
        """

        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ':' in decoded_base64_authorization_header:
            return tuple(decoded_base64_authorization_header.split(':'))

        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):  # type: ignore

        """
        returns the User instance based on his email and password
        """

        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        users = User.search({"email": user_email})

        if not users or len(users) == 0:
            return None

        """ assume the first user found is the correct one"""
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user
