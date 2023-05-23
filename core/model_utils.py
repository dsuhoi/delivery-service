from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .database import Base
from .models import Cargo, Location


async def get_zip_codes(db: AsyncSession):
    return (
        await db.scalars(text(rf'SELECT zip FROM "{Location.__tablename__}";'))
    ).all()


async def get_count(db: AsyncSession, model: Base):
    return (await db.scalars(func.count(model.id))).first()


async def get_by_id(db: AsyncSession, model: Base, id: int):
    return (await db.scalars(select(model).where(model.id == id))).first()


async def get_all(db: AsyncSession, model: Base):
    return (await db.scalars(select(model))).all()
