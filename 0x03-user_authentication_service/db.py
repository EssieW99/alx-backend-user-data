#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict, Any


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        saves the user to the database.
        """

        new_user = User(email=email, hashed_password=hashed_password)

        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """
        finds a user by the use of arbitrary keyword arguments
        """

        session = self._session

        required_key = {'email'}
        wrong_keys = required_key - set(kwargs.keys())
        if wrong_keys:
            raise InvalidRequestError()

        user = session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound("No user found")

        return user
