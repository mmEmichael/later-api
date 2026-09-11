from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from later_api.api.resources import router as resources_router
from later_api.config import settings
from later_api.database.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore[reportUnusedParameter]
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resources_router)


def run() -> None:
    import uvicorn

    uvicorn.run("later_api.main:app", host="0.0.0.0", port=8000, reload=True)
