from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from psycopg_pool import AsyncConnectionPool

from . import constants
from .routers import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = AsyncConnectionPool(conninfo=constants.POSTGRES_CONNECTION_STRING)
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(health.router)
