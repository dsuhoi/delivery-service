import core.models as models
import core.schemas as schemas
import strawberry
from core.database import get_session
from core.model_utils import get_all, get_by_id, get_location
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info


async def get_context(db: AsyncSession = Depends(get_session)):
    return {"db": db}


def from_pydantic(cls, model):
    """Legacy code to fix bugs with pydantic v2.x.x"""
    return cls(**model.model_dump())


# @strawberry.experimental.pydantic.type(model=schemas.Location)
@strawberry.type
class Location:
    zip: schemas.Zip  # strawberry.auto
    city: str  # strawberry.auto
    state_name: str  # strawberry.auto
    lat: float
    lng: float


# @strawberry.experimental.pydantic.type(model=schemas.CarFull, all_fields=True)
@strawberry.type
class Car:
    id: int
    car_number: schemas.CarNumber
    loc: Location
    load_capacity: schemas.Weight


# @strawberry.experimental.pydantic.type(model=schemas.CargoFull)
@strawberry.type
class Cargo:
    id: int  # strawberry.auto
    pick_up_loc: Location  # strawberry.auto
    delivery_loc: Location  # strawberry.auto
    weight: schemas.Weight  # strawberry.auto
    description: str


@strawberry.type
class Query:
    @strawberry.field
    async def cars(self, info: Info) -> list[Car]:
        return [
            schemas.CarFull.parse_obj(c)
            for c in await get_all(info.context["db"], models.Car)
        ]

    @strawberry.field
    async def get_car(self, info: Info, id: int) -> Car | None:
        return schemas.CarFull.parse_obj(
            await get_by_id(info.context["db"], models.Car, id=id)
        )

    @strawberry.field
    async def cargo(self, info: Info) -> list[Cargo]:
        return [
            schemas.CargoFull.parse_obj(c)
            for c in await get_all(info.context["db"], models.Cargo)
        ]

    @strawberry.field
    async def location(self, info: Info, zip: schemas.Zip) -> Location | None:
        return schemas.Location.parse_obj(await get_location(info.context["db"], zip))


schema = strawberry.Schema(query=Query, types=[Cargo, Car, Location])
router = GraphQLRouter(schema, context_getter=get_context)
