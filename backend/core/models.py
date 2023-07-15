import random

import geoalchemy2 as gsa
import sqlalchemy as sa
from geopy.distance import distance as geodist
from shapely.geometry import Point

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

    pick_up_loc = sa.orm.relationship(
        "Location", foreign_keys=[pick_up], lazy="selectin"
    )
    delivery_loc = sa.orm.relationship(
        "Location", foreign_keys=[delivery], lazy="selectin"
    )

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

    loc = sa.orm.relationship("Location", foreign_keys=[current_loc], lazy="selectin")

    def __str__(self):
        return f"id={self.id} # car_number={self.car_number} # location={self.loc}"


class Location(Base):
    __tablename__ = "locations"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    zip = sa.Column(sa.Integer, unique=True, index=True, nullable=False)
    city = sa.Column(sa.String(32), nullable=False)
    state_name = sa.Column(sa.Text, nullable=False)
    geo = sa.Column(gsa.Geometry(geometry_type="POINT", srid=4326), nullable=False)
    # lat = sa.Column(sa.Float, nullable=False)
    # lng = sa.Column(sa.Float, nullable=False)

    @staticmethod
    def from_dict(data: dict) -> "Location":
        return Location(
            zip=data["zip"],
            city=data["city"],
            state_name=data["state_name"],
            geo=gsa.shape.from_shape(Point(data["lat"], data["lng"]), srid=4326),
        )

    def to_dict(self) -> dict:
        lat, lng = self.coords
        return {
            "zip": self.id,
            "city": self.city,
            "state_name": self.state_name,
            "lat": lat,
            "lng": lng,
        }

    @property
    def coords(self) -> (float, float):
        coord = gsa.shape.to_shape(self.geo)
        return (coord.x, coord.y)

    def distance(self, loc: "Location") -> float:
        return round(geodist(self.coords, loc.coords).miles, 4)

    def __str__(self):
        return f"zip[{self.lat}, {self.lng}]: {self.zip} # {self.city}"
