from contextlib import asynccontextmanager

from fastapi import FastAPI

from later_api.api.resources import router as resources_router
from later_api.database.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore[reportUnusedParameter]
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(resources_router)
