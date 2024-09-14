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
