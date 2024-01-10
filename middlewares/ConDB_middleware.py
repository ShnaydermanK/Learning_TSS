from collections.abc import Callable, Awaitable
from typing import Any

import asyncpg.pool
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from Sql import Request


class DBSession(BaseMiddleware):
    def __init__(self, conn: asyncpg.pool.Pool):
        super().__init__()
        self.conn = conn

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.conn.acquire() as conn:
            data['request'] = Request(conn)
            return await handler(event, data)
