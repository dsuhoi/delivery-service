from typing import Annotated

import core.models as models
import core.schemas as schemas
import sqlalchemy as sa
from core.database import get_session
from core.model_utils import (create_model, delete_model, get_all, get_by_id,
                              get_cargo_with_count_cars, get_zip_codes)
from core.models import Car, Cargo, Location
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cargo", tags=["cargo"])


async def get_id_cargo(cargo_id: int, db: AsyncSession = Depends(get_session)):
    if cargo_db := await get_by_id(db, models.Cargo, cargo_id):
        return cargo_db
    else:
        raise HTTPException(status_code=404, detail="There is no cargo for such id.")


@router.post("/", response_model=schemas.CargoResponse, description="Создание груза.")
async def create_cargo(
    cargo: schemas.CargoParams, db: AsyncSession = Depends(get_session)
):
    if not ({cargo.pick_up, cargo.delivery} < set(await get_zip_codes(db))):
        raise HTTPException(
            status_code=400,
            detail="There are no zip codes for 'pick_up' or 'delivery' in the database.",
        )
    db_cargo = models.Cargo(**cargo.dict())
    await create_model(db, db_cargo)
    return db_cargo


@router.get(
    "/",
    response_model=list[schemas.CargoList],
    description="Получение списка грузов и машин рядом с ними.",
)
async def list_cargo(
    weight: Annotated[
        int | None,
        Query(
            description="Фильтр по весу груза",
        ),
    ] = 0,
    distance: Annotated[
        float | None, Query(example=450.0, description="Фильтр по дистанции (км)")
    ] = 450,
    db: AsyncSession = Depends(get_session),
):
    return await get_cargo_with_count_cars(db, distance, weight)


@router.get(
    "/{cargo_id}",
    response_model=schemas.CargoGet,
    description="Получение полной информации о грузе.",
)
async def get_cargo(
    cargo: models.Cargo = Depends(get_id_cargo), db: AsyncSession = Depends(get_session)
):
    cars_db = await get_all(db, models.Car)
    cars = []
    for car in cars_db:
        dist = cargo.pick_up_loc.distance(car.loc)
        cars.append(
            schemas.CarWithDistance(id=car.id, car_number=car.car_number, distance=dist)
        )
    return schemas.CargoGet(
        id=cargo.id,
        pick_up=cargo.pick_up,
        delivery=cargo.delivery,
        weight=cargo.weight,
        description=cargo.description,
        cars=cars,
    )


@router.patch(
    "/", response_model=schemas.CargoResponse, description="Обновление данных груза."
)
async def update_cargo(
    cargo: schemas.CargoPatch,
    cargo_db: models.Cargo = Depends(get_id_cargo),
    db: AsyncSession = Depends(get_session),
):
    if cargo.weight:
        cargo_db.weight = cargo.weight
    if cargo.description:
        cargo_db.description = cargo.description
    await db.commit()
    return cargo_db


@router.delete(
    "/{cargo_id}", response_model=schemas.CargoDelete, description="Удаление груза."
)
async def delete_cargo(
    cargo: models.Cargo = Depends(get_id_cargo), db: AsyncSession = Depends(get_session)
):
    await delete_model(db, cargo)
    return {"detail": "Cargo deleted"}
