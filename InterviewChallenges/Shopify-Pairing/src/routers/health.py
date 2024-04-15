from psycopg_pool import AsyncConnectionPool
from fastapi import APIRouter, Request

from ..repository import status_repository

router = APIRouter()

@router.get('/health')
async def get_health(request: Request):
    db_pool: AsyncConnectionPool = request.app.state.db_pool
    return { 'db_status': await status_repository.get_pg_connection_status(db_pool) }
