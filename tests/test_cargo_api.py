import pytest
from core.models import Car, Cargo, Location

from tests.conftest import async_session_test


@pytest.fixture(scope="session")
async def create_data():
    async with async_session_test() as db:
        loc_data = [
            [58045, "Hillsboro", "North Dakota", 47.38241, -97.02686],
            [15951, "Saint Michael", "Pennsylvania", 40.3307, -78.77209],
            [84076, "Tridell", "Utah", 40.44718, -109.84017],
            [5446, "Colchester", "Vermont", 44.5541, -73.21647],
            [12933, "Ellenburg", "New York", 44.89118, -73.84512],
            [50472, "Saint Ansgar", "Iowa", 43.42265, -92.94644],
            [34470, "Ocala", "Florida", 29.20098, -82.08262],
            [39092, "Lake", "Mississippi", 32.31489, -89.36833],
        ]

        loc_models = [
            Location(zip=d[0], city=d[1], state_name=d[2], lat=d[3], lng=d[4])
            for d in loc_data
        ]
        db.add_all(loc_models)

        car_data = [
            ["9218C", 58045, 215],
            ["4075H", 15951, 425],
            ["1225K", 5446, 892],
            ["3863F", 12933, 416],
        ]

        car_models = [
            Car(car_number=d[0], current_loc=d[1], load_capacity=d[2]) for d in car_data
        ]
        db.add_all(car_models)

        cargo_data = [
            [12933, 58045, 123, "Text1"],
            [58045, 12933, 250, "Text2"],
            [15951, 58045, 123, "Text3"],
        ]

        cargo_models = [
            Cargo(pick_up=d[0], delivery=d[1], weight=d[2], description=d[3])
            for d in cargo_data
        ]
        db.add_all(cargo_models)
        await db.commit()
        print("DATA LOADED")


async def test_list_cargo(ac, create_data):
    response = await ac.get("cargo/", params={"distance": 450})
    assert response.status_code == 200
    assert response.json()[0] == {
        "count_cars_nerby": 3,
        "delivery": 58045,
        "id": 1,
        "pick_up": 12933,
    }
