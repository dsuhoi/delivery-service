import core.models as models
import core.schemas as schemas
from core.database import get_session
from core.model_utils import get_all
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/geo", tags=["geo"])


@router.get("/", description="Получение всех данных о местоположении объектов.")
async def get_geo(db: AsyncSession = Depends(get_session)):
    cargo = [
        schemas.CargoLocation(
            id=cg.id,
            pick_up=cg.pick_up_loc,
            delivery=cg.delivery_loc,
            description=cg.description,
        )
        for cg in await get_all(db, models.Cargo)
    ]
    cars = [
        schemas.CarLocation(car_number=car.car_number, location=car.loc)
        for car in await get_all(db, models.Car)
    ]
    return schemas.GeoResponse(cargo=cargo, cars=cars)
