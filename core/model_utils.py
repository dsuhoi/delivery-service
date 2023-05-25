from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .database import Base, engine
from .models import Car, Location


async def get_zip_codes(db: AsyncSession):
    return (await db.scalars(select(Location.zip))).all()


async def get_count(db: AsyncSession, model: Base):
    return (await db.scalars(func.count(model.id))).first()


async def get_by_id(db: AsyncSession, model: Base, id: int):
    return (await db.scalars(select(model).where(model.id == id))).first()


async def get_all(db: AsyncSession, model: Base):
    return (await db.scalars(select(model))).all()


async def update_cars_position_random():
    query = update(Car).values(
        current_loc=select(Location.zip).order_by(func.random() + Car.id).limit(1)
    )
    async with engine.begin() as conn:
        await conn.execute(query)
