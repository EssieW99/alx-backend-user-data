#!/usr/bin/env python3
""" Basic Auth"""

from api.v1.auth.auth import Auth
import base64
import binascii


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
