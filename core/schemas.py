from typing import Annotated

from pydantic import BaseModel, Field

Zip = Annotated[
    int, Field(ge=0, le=99999, example="705", description="Zip код локации")
]
# regex=r"^\d{1,5}$",

Weight = Annotated[int, Field(ge=1, le=1000, example=123, description="Вес груза")]
Description = Annotated[
    str, Field(example="Text about cargo...", description="Описание груза")
]


class CargoBase(BaseModel):
    pick_up: Zip
    delivery: Zip
    weight: Weight
    description: Description


class CargoResponse(CargoBase):
    id: int

    class Config:
        orm_mode = True


class CargoPatch(BaseModel):
    weight: Weight = None
    description: Description = None


CarNumber = Annotated[
    str,
    Field(regex=r"^[1-9]\d{3}[A-Z]$", example="1234A", description="Номер автомобиля"),
]


class Car(BaseModel):
    id: int
    car_number: CarNumber
    current_loc: Zip
    load_capacity: Weight


class CarResponse(Car):
    class Config:
        orm_mode = True


class CarPatch(BaseModel):
    current_loc: Zip = None
    load_capacity: Weight = None
