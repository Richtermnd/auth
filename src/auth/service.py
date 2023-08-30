from datetime import datetime, timedelta
import logging

from fastapi import HTTPException, status
from sqlalchemy import select
from jose import jwt

from . import models, schemas
from .. import database
from ..config import settings


logger = logging.getLogger(__name__)


async def create_user(
        item: schemas.CreateUser,
        session: database.AsyncSession
    ):
    """Create user."""
    db_item = models.User(**item.model_dump(exclude={'repeat_password'}))
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    logging.info(f'User {db_item.username} registred with id {db_item.id}')
    return db_item


async def get_user_by_username(
        username: str,
        session: database.AsyncSession
    ):
    """Get user by username."""
    logger.debug(f'Get user with username {username}')
    stmt = select(models.User).where(models.User.username == username)
    user = (await session.execute(stmt)).scalar()
    return user


async def get_users(
        session: database.AsyncSession
    ):
    """Get all users."""
    stmt = select(models.User)
    users = (await session.execute(stmt)).scalars()
    return users


async def authenticate_user(
        login_user: schemas.LoginUser,
        session: database.AsyncSession
    ):
    """Authenticate user."""
    user = await get_user_by_username(login_user.username, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username doesn\'t exist."
        )
    if not user.check_password(login_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password."
        )
    return user


async def create_token(
        user: models.User
    ) -> schemas.Token:
    """Create token."""
    data = user.token_data()
    exp = datetime.utcnow() + timedelta(hours=1)
    data["exp"] = exp
    encoded_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return schemas.Token(access_token=encoded_token)
