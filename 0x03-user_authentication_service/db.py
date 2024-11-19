#!/usr/bin/env python3
"""DB module
"""

import bcrypt
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

    def find_user_by(self, **kwargs: Any) -> User:
        """
        finds a user by the use of arbitrary keyword arguments
        """

        session = self._session

        try:

            user = session.query(User).filter_by(**kwargs).first()
            return user
        except NoResultFound:
            raise NoResultFound("User not found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid")

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """
        locates a user then updates the user's attributes
        as passed in the method's arguments
        """

        session = self._session
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("Error")

            setattr(user, key, value)

        session.commit()
        return None
