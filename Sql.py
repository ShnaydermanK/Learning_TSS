import asyncpg


class Request:
    def __init__(self, conn: asyncpg.pool.Pool):
        self.conn = conn

    async def create_table(self):  # Исправлено название метода
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS learning_tss (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                chat_name VARCHAR(255),
                user_id BIGINT,
                username VARCHAR(255),
                mess VARCHAR(255),
                date TIMESTAMPTZ,
                text TEXT
            )
        ''')

    async def insert_history(self, chat_id, chat_name, user_id, username,mess, date, text):
        await self.conn.execute(
            "INSERT INTO learning_tss (chat_id, chat_name, user_id, username,mess, date, text) VALUES ($1, $2, $3, $4, $5, $6, $7)",
            chat_id, chat_name, user_id, username, mess,date, text
        )

    async def creat_table_history(self):

        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS chat_history_learning (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                chat_name VARCHAR(255),
                user_id BIGINT,
                username VARCHAR(255),
                date TIMESTAMPTZ,
                text TEXT
            )
        ''')

    async def insert_table_history(self,chat_id,chat_name, user_id, username, date, text):

        await self.conn.execute(
            "INSERT INTO chat_history_learning (chat_id, chat_name, user_id, username, date, text) VALUES ($1, $2, $3, $4, $5, $6)",
            chat_id, chat_name, user_id, username, date, text
        )

    async def creat_table_stop_slova(self):
        await self.conn.execute('''
               CREATE TABLE IF NOT EXISTS chat_history_stop_slova (
                   id SERIAL PRIMARY KEY,
                   chat_id BIGINT,
                   chat_name VARCHAR(255),
                   user_id BIGINT,
                   username VARCHAR(255),
                   date TIMESTAMPTZ,
                   text TEXT
               )
           ''')

    async def insert_table_stop_slova(self, chat_id, chat_name, user_id, username, date, text):
        await self.conn.execute(
            "INSERT INTO chat_history_stop_slova (chat_id, chat_name, user_id, username, date, text) VALUES ($1, $2, $3, $4, $5, $6)",
            chat_id, chat_name, user_id, username, date, text
        )
