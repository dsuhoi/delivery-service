from typing import Annotated

from pydantic import BaseModel, Field

Zip = Annotated[
    int, Field(ge=0, le=99999, example="705", description="Это zip код локации")
]
# regex=r"^\d{1,5}$",


class Cargo(BaseModel):
    pick_up: Zip
    delivery: Zip
    weight: int = Field(ge=1, le=1000, example=123, description="Вес груза")
    description: str = Field(
        example="Text about cargo...", description="Описание груза"
    )


class CargoPatch(BaseModel):
    weight: int = Field(ge=1, le=1000, example=123, description="Вес груза")
    description: str = Field(
        example="Text about cargo...", description="Описание груза"
    )
