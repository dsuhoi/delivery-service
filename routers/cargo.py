import logging
from typing import Annotated

from core.database import get_session
from core.schemas import Cargo
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cargo", tags=["cargo"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=Cargo)
async def create_cargo(cargo: Cargo, db: AsyncSession = Depends(get_session)):
    logger.info("Hey!")
    return Cargo(pick_up=12, delivery=15, weight=100, description="HELLO!!")


@router.get("/", description="Получение списка грузов и машин рядом с ними")
async def list_cargo(
    weight: Annotated[int | None, Query(description="Фильтр по весу груза")] = None,
    distance: Annotated[
        float | None, Query(description="Фильтр ближайших машин по дистанции (мили)")
    ] = None,
    db: AsyncSession = Depends(get_session),
):
    pass


@router.get("/{cargo_id}")
async def get_cargo(cargo_id: int, db: AsyncSession = Depends(get_session)):
    pass


@router.patch("/")
async def update_cargo(
    cargo_id: int, cargo: Cargo, db: AsyncSession = Depends(get_session)
):
    pass


@router.delete("/{cargo_id}")
async def delete_cargo(cargo_id: int, db: AsyncSession = Depends(get_session)):
    pass
