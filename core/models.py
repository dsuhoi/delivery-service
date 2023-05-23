import sqlalchemy as sa

from .database import Base


class Cargo(Base):
    __tablename__ = "cargo"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    pick_up = sa.Column(
        sa.ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    delivery = sa.Column(
        sa.ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    weight = sa.Column(sa.Integer)
    description = sa.Column(sa.Text)


class Car(Base):
    __tablename__ = "cars"
    # id = sa.Column(sa.Integer, primary_key=True, index=True)
    uuid = sa.Column(sa.String(32), primary_key=True, index=True)
    current_loc = sa.Column(
        sa.ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    load_capacity = sa.Column(sa.Integer)


class Location(Base):
    __tablename__ = "locations"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    city = sa.Column(sa.String(32))
    zip = sa.Column(sa.Integer, unique=True)
    state_name = sa.Column(sa.Text)
    lat = sa.Column(sa.Float)
    lng = sa.Column(sa.Float)
