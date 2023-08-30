from typing import Annotated
import logging

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from . import schemas, service, models
from .. import database
from ..config import settings

logger = logging.getLogger(__name__)

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


async def get_valid_register_user(
    user: schemas.CreateUser,
    session: database.InjectionSession
    ) -> schemas.CreateUser:
    """Validate register user data"""
    # Validate username
    if user.username == 'me':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid username.'
        )
     
    db_user = await service.get_user_by_username(user.username, session)
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this username already exist.'
        )

    # Check passwords   
    if user.password != user.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Passwords doesn\'t match.'
        )
    return user


async def get_login_user(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()]
    ) -> schemas.LoginUser:
    """Get login user pydantic from form"""
    return schemas.LoginUser(username=username, password=password)


async def get_current_user(
        token: Annotated[str, Depends(_oauth2_scheme)],
        session: database.InjectionSession
    ):
    """Get current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.debug('Get current user.')
    try:
        # Get payload from jwt token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from payload
    user = await service.get_user_by_username(username, session)
    logger.debug(f'Current user {user}')
    if user is None:
        raise credentials_exception
    return user


InjectionCurrentUser = Annotated[models.User, Depends(get_current_user)]