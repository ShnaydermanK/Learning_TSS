import asyncpg
from config import config


async def create_database_pools():
    create_pool = await \
        asyncpg.create_pool(
            user=config.dbp.db_user,
            password=config.dbp.db_password,
            database=config.dbp.database,
            host=config.dbp.db_host,
            port=config.dbp.db_port)

    return create_pool