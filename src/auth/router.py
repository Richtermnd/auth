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
    db_user = await service.create_user(user, session)
    return db_user


@router.get(
        '/{username}', 
        response_model=schemas.User
        )
async def user(
        username: Annotated[str, Path()],
        session: database.InjectionSession
    ):
    return await service.get_user_by_username(username, session)


@router.get(
        '/', 
        response_model=list[schemas.User]
        )
async def user(
        session: database.InjectionSession
    ):
    return await service.get_users(session)

