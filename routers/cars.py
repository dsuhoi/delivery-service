import core.models as models
import core.schemas as schemas
from core.database import get_session
from core.model_utils import get_all, get_by_id, get_zip_codes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cars", tags=["cars"])


async def get_id_car(car_id: int, db: AsyncSession = Depends(get_session)):
    if car_db := await get_by_id(db, models.Car, car_id):
        return car_db
    else:
        raise HTTPException(status_code=404, detail="There is no car for such id")


# @router.post("/")
# async def create_car(db: AsyncSession = Depends(get_session)):
#     pass


@router.get("/", response_model=list[schemas.CarResponse])
async def list_car(db: AsyncSession = Depends(get_session)):
    return await get_all(db, models.Car)


@router.patch("/")
async def update_car(
    car: schemas.CarPatch,
    car_db: models.Car = Depends(get_id_car),
    db: AsyncSession = Depends(get_session),
):
    if car.current_loc and (car.current_loc in await get_zip_codes(db)):
        car_db.current_loc = car.current_loc
