from typing import Annotated

import core.models as models
import core.schemas as schemas
from core.database import get_session
from core.model_utils import get_by_id, get_zip_codes
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cargo", tags=["cargo"])


async def get_id_cargo(cargo_id: int, db: AsyncSession = Depends(get_session)):
    if cargo_db := await get_by_id(db, models.Cargo, cargo_id):
        return cargo_db
    else:
        raise HTTPException(status_code=404, detail="There is no cargo for such id")


@router.post("/", response_model=schemas.CargoResponse, description="Создание груза.")
async def create_cargo(
    cargo: schemas.CargoBase, db: AsyncSession = Depends(get_session)
):
    if not ({cargo.pick_up, cargo.delivery} < set(await get_zip_codes(db))):
        raise HTTPException(
            status_code=400,
            detail="There are no zip codes for 'pick_up' or 'delivery' in the database.",
        )
    db_cargo = models.Cargo(**cargo.dict())
    db.add(db_cargo)
    print(db_cargo)
    await db.commit()
    return db_cargo


@router.get(
    "/",
    response_model=list[schemas.CargoResponse],
    description="Получение списка грузов и машин рядом с ними.",
)
async def list_cargo(
    weight: Annotated[int | None, Query(description="Фильтр по весу груза")] = None,
    distance: Annotated[
        float | None, Query(description="Фильтр ближайших машин по дистанции (мили)")
    ] = None,
    db: AsyncSession = Depends(get_session),
):
    pass


@router.get("/{cargo_id}", description="Получение полной информации о грузе.")
async def get_cargo(
    cargo: models.Cargo = Depends(get_id_cargo), db: AsyncSession = Depends(get_session)
):
    pass


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


@router.delete("/{cargo_id}", description="Удаление груза.")
async def delete_cargo(
    cargo: models.Cargo = Depends(get_id_cargo), db: AsyncSession = Depends(get_session)
):
    await db.delete(cargo)
    await db.commit()
    return {"detail": "Cargo deleted"}
