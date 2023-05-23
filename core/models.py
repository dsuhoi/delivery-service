import random

import sqlalchemy as sa

from .database import Base


class Cargo(Base):
    __tablename__ = "cargo"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    pick_up = sa.Column(
        sa.ForeignKey("locations.zip", ondelete="SET NULL"), nullable=True
    )
    delivery = sa.Column(
        sa.ForeignKey("locations.zip", ondelete="SET NULL"), nullable=True
    )
    weight = sa.Column(sa.Integer, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def __str__(self):
        return f"id={self.id} # weight={self.weight} # delivery={self.delivery}"


class Car(Base):
    __tablename__ = "cars"

    @staticmethod
    def generate_car_number():
        return str(random.randint(1000, 9999)) + random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    car_number = sa.Column(
        sa.String(5), unique=True, nullable=False, default=generate_car_number
    )
    current_loc = sa.Column(
        sa.ForeignKey("locations.zip", ondelete="SET NULL"), nullable=True
    )
    load_capacity = sa.Column(
        sa.Integer, nullable=False, default=lambda: random.randint(1, 1000)
    )

    def __str__(self):
        return f"id={self.id} # car_number={self.car_number} # location={self.location}"


class Location(Base):
    __tablename__ = "locations"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    zip = sa.Column(sa.Integer, unique=True, index=True, nullable=False)
    city = sa.Column(sa.String(32), nullable=False)
    state_name = sa.Column(sa.Text, nullable=False)
    lat = sa.Column(sa.Float, nullable=False)
    lng = sa.Column(sa.Float, nullable=False)

    def __str__(self):
        return f"zip[{self.lat}, {self.lng}]: {self.zip} # {self.city}"
