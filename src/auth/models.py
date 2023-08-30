from sqlalchemy import Boolean, Column, Integer, String

from . import utils
from .. import database


class UserMixin:
    """Mixin for create User model

    Use this mixin to create custom user model.

    class MyUser(UserMixin, DeclarativeBase):
        pass
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    def check_password(self, raw_password: str) -> bool:
        return False

    @property
    def password(self) -> str:
        raise AttributeError

    @password.setter
    def password(self, value: str) -> None:
        raise AttributeError
    
    def __str__(self) -> str:
        return self.username


class User(UserMixin, database.Base):
    def check_password(self, raw_password: str) -> bool:
        return utils.verify_password(raw_password, self.hashed_password)

    @property
    def password(self) -> str:
        return self.hashed_password

    @password.setter
    def password(self, value: str) -> None:
        self.hashed_password =  utils.hash_password(value)
    

    def token_data(self) -> dict:
        data = {
            'id': self.id,
            'sub': self.username
        }
        return data
