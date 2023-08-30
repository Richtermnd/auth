import logging

from sqlalchemy import select

from . import models, schemas
from .. import database


logger = logging.getLogger(__name__)


async def create_user(
        item: schemas.CreateUser,
        session: database.AsyncSession
    ):
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
    stmt = select(models.User).where(models.User.username == username)
    user = (await session.execute(stmt)).scalar()
    return user


async def get_users(
        session: database.AsyncSession
    ):
    stmt = select(models.User)
    users = (await session.execute(stmt)).scalars()
    return users
