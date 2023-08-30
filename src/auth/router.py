from typing import Annotated
import logging

from fastapi import APIRouter, Depends, Path

from . import schemas, service, dependencies
from .. import database


router = APIRouter(
    prefix='/users',
    tags=['users']
)
logger = logging.getLogger(__name__)


@router.post(
        '/register', 
        response_model=schemas.User
        )
async def register(
    user: Annotated[schemas.CreateUser, Depends(dependencies.get_valid_register_user)],
    session: database.InjectionSession
    ):
    """Registration endpoint."""
    db_user = await service.create_user(user, session)
    return db_user


@router.get(
    '/me',
    response_model=schemas.User
    )
async def me(
    current_user: dependencies.InjectionCurrentUser
    ):
    """Current user endpoint."""
    logging.info(current_user)
    return current_user


@router.get(
        '/{username}', 
        response_model=schemas.User
        )
async def user(
        username: Annotated[str, Path()],
        session: database.InjectionSession
    ):
    """Get user by username."""
    return await service.get_user_by_username(username, session)


@router.get(
        '/', 
        response_model=list[schemas.User]
        )
async def user(
        session: database.InjectionSession
    ):
    """Get all users."""
    return await service.get_users(session)


@router.post(
        '/auth',
        response_model=schemas.Token,
        )
async def token(
        login_user: Annotated[schemas.LoginUser, Depends(dependencies.get_login_user)],
        session: database.InjectionSession
    ):
    """Generate JWT token."""
    user = await service.authenticate_user(login_user, session)
    token = await service.create_token(user)
    return token
