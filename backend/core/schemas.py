from typing import Annotated

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, SkipValidation
from shapely import Point

# import core.models as models

Zip = Annotated[int, Field(ge=0, le=99999, example=705, description="Zip код локации")]

Weight = Annotated[int, Field(ge=1, le=1000, example=123, description="Вес груза")]
Description = Annotated[
    str, Field(example="Text about cargo...", description="Описание груза")
]

CarNumber = Annotated[
    str,
    Field(
        pattern=r"^[1-9]\d{3}[A-Z]$", example="1234A", description="Номер автомобиля"
    ),
]

Lat = Annotated[float, Field(example=10.345, description="Широта")]
Lng = Annotated[float, Field(example=10.345, description="Долгота")]


def ewkb_to_wkt(geom: WKBElement):
    return to_shape(geom).wkt


class Location(BaseModel):
    zip: Zip
    city: str = Field(example="New York", description="Название города")
    state_name: str = Field(example="Texas", description="Название штата")
    lat: Lat
    lng: Lng

    @staticmethod
    def from_orm(base):
        pass

    class Config:
        from_attributes = True


class Car(BaseModel):
    id: int
    car_number: CarNumber
    current_loc: Zip
    load_capacity: Weight


class CarFull(BaseModel):
    id: int
    car_number: CarNumber
    loc: Location
    load_capacity: Weight

    class Config:
        from_attributes = True


class CarResponse(Car):
    class Config:
        from_attributes = True


class CarPatch(BaseModel):
    current_loc: Zip = None
    load_capacity: Weight = None


class CarWithDistance(BaseModel):
    id: int
    car_number: CarNumber
    distance: float = Field(example="10.11", description="Расстояние до груза")


class Cargo(BaseModel):
    _id: int
    pick_up: Zip
    delivery: Zip
    weight: Weight
    description: Description


class CargoFull(BaseModel):
    id: int
    pick_up_loc: Location
    delivery_loc: Location
    weight: Weight
    description: Description

    class Config:
        from_attributes = True


class CargoParams(Cargo):
    pass


class CargoResponse(Cargo):
    id: int

    class Config:
        from_attributes = True


class CargoGet(CargoResponse):
    cars: list[CarWithDistance]


class CargoPatch(BaseModel):
    weight: Weight = None
    description: Description = None


class CargoList(BaseModel):
    id: int
    pick_up: Zip
    delivery: Zip
    count_cars_nerby: int = Field(example=10, description="Количество машин рядом")


class CargoDelete(BaseModel):
    detail: str = Field(example="status")


class CarLocation(BaseModel):
    car_number: CarNumber
    loc: Location

    class Config:
        from_attributes = True


class CargoLocation(BaseModel):
    id: int
    pick_up_loc: Location
    delivery_loc: Location
    description: Description

    class Config:
        from_attributes = True


class GeoResponse(BaseModel):
    cars: list[CarLocation]
    cargo: list[CargoLocation]
