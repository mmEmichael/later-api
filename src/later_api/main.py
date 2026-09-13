from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from later_api.api.resources import router as resources_router
from later_api.config import settings

app = FastAPI()

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
