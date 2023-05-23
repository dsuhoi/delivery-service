import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.database import init_db
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


@app.get("/")
async def root():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
