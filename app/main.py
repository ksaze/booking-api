from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1 import router as api_router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Fitness Booking API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)
