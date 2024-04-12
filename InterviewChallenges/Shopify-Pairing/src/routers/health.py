from psycopg_pool import AsyncConnectionPool
from fastapi import APIRouter, Request

router = APIRouter()

@router.get('/health')
async def get_health(request: Request):
    db_pool: AsyncConnectionPool = request.app.state.db_pool
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('select 1;')
            return { 'db_status': bool(await cur.fetchone()) }
