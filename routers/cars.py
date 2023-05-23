from core.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("/")
async def create_car(db: AsyncSession = Depends(get_session)):
    pass


@router.patch("/")
async def update_car(location, db: AsyncSession = Depends(get_session)):
    pass
