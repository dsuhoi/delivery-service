import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every

from core.database import init_db
from core.init_data_db import init_data
from core.model_utils import update_cars_position_random
from routers import cargo, cars

app = FastAPI(
    title="Delivery Service",
    description="Сервис поиска ближайших машин для перевозки грузов",
    version="1.0.1",
    license_info={"name": "MIT License", "url": "https://mit-license.org/"},
)
app.include_router(cargo.router)
app.include_router(cars.router)


@app.on_event("startup")
async def on_startup():
    await init_db()
    await init_data()


@app.on_event("startup")
@repeat_every(seconds=3 * 60, wait_first=True)
async def update_data():
    await update_cars_position_random()


@app.get("/")
async def root():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
