from psycopg_pool import AsyncConnectionPool

async def get_pg_connection_status(db_pool: AsyncConnectionPool) -> bool:
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('select 1;')
            return bool(await cur.fetchone())
