from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from sqlalchemy import select, update, delete
from datetime import datetime, date, timedelta


async def orm_add_user(session: AsyncSession, user_id):
    session.add(User(
        tg_id=user_id
    ))
    await session.commit()


async def orm_get_user(session: AsyncSession, user_id):
    query = select(User).where(User.tg_id == user_id)
    res = await session.execute(query)
    return res.scalar()


async def orm_get_all_users(session: AsyncSession):
    query = select(User)
    res = await session.execute(query)
    return res.scalars().all()


async def orm_update_status(session: AsyncSession, user_id, status):
    query = update(User).where(User.tg_id == user_id).values(
        monkey_status=status
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_user(session: AsyncSession, user_id):
    query = delete(User).where(User.tg_id == user_id)
    await session.execute(query)
    await session.commit()
