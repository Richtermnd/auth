from fastapi import HTTPException, status

from . import schemas, service
from .. import database


async def get_valid_register_user(
    user: schemas.CreateUser,
    session: database.InjectionSession
    ):
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
    if user.password != user.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Passwords doesn\'t match.'
        )
    return user


