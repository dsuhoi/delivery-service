from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .database import Base, engine
from .models import Car, Cargo, Location


async def get_zip_codes(db: AsyncSession):
    return (await db.scalars(select(Location.zip))).all()


async def get_count(db: AsyncSession, model: Base):
    return (await db.scalars(func.count(model.id))).first()


async def get_by_id(db: AsyncSession, model: Base, id: int):
    return (await db.scalars(select(model).where(model.id == id))).first()


async def get_all(db: AsyncSession, model: Base):
    return (await db.scalars(select(model))).all()


async def get_location(db: AsyncSession, zip: int):
    return (await db.scalars(select(Location).where(Location.zip == zip))).first()


async def get_cargo_with_count_cars(db: AsyncSession, distance: float, weight: int):
    subquery_cars = (
        select(Car, Location.geom.label("loc"))
        .join(Location, Car.current_loc == Location.zip)
        .subquery()
    )
    subquery_cargo = (
        select(Cargo, Location.geom.label("loc"))
        .join(Location, Cargo.pick_up == Location.zip)
        .subquery()
    )
    query = (
        select(
            subquery_cargo.c.id.label("id"),
            subquery_cargo.c.pick_up.label("pick_up"),
            subquery_cargo.c.delivery.label("delivery"),
            func.count(subquery_cars.c.id).label("count_cars_nearby"),
        )
        .outerjoin(
            subquery_cars,
            func.ST_DWithin(subquery_cargo.c.loc, subquery_cars.c.loc, 0.01 * distance),
        )
        .where(subquery_cargo.c.weight > weight)
        .group_by(
            subquery_cargo.c.id, subquery_cargo.c.pick_up, subquery_cargo.c.delivery
        )
    )
    return [
        {"id": r[0], "pick_up": r[1], "delivery": r[2], "count_cars_nerby": r[3]}
        for r in await db.execute(query)
    ]


async def update_cars_position_random():
    query = update(Car).values(
        current_loc=select(Location.zip).order_by(func.random() + Car.id).limit(1)
    )
    async with engine.begin() as conn:
        await conn.execute(query)


async def create_model(db: AsyncSession, model: Base):
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


async def delete_model(db: AsyncSession, model: Base):
    await db.delete(model)
    await db.commit()
