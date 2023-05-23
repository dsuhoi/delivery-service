import asyncio
import random

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session, init_db
from .model_utils import get_count, get_zip_codes
from .models import Car, Location


async def init_locations(db: AsyncSession) -> list[int]:
    loc_df = pd.read_csv("locations.csv")
    db.add_all([Location(**loc) for loc in loc_df.to_dict("index").values()])
    await db.commit()
    return loc_df["zip"].to_list()


async def init_cars(db: AsyncSession, number: int = 20):
    zips = await get_zip_codes(db)
    db.add_all([Car(current_loc=random.choice(zips)) for _ in range(number)])
    await db.commit()


async def init_data():
    db = await anext(get_session())
    if (await get_count(db, Location)) == 0:
        await init_locations(db)
    if (await get_count(db, Car)) == 0:
        await init_cars(db, 20)


async def _init_all_db():
    await init_db()
    await init_data()


if __name__ == "__main__":
    asyncio.run(_init_all_db())
