from dataclasses import dataclass
from environs import Env

env: Env = Env()
env.read_env()


@dataclass(slots=True, frozen=True)
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str
    db_port: str





@dataclass(slots=True, frozen=True)
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass(slots=True, frozen=True)
class Config:
    tg_bot: TgBot
    dbp: DatabaseConfig



config = Config(
    tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS')))
    ),
    dbp=DatabaseConfig(
        database=env('DATABASE_PORTAL'),
        db_host=env('DB_HOST_PORTAL'),
        db_user=env('DB_USER_PORTAL'),
        db_password=env('DB_PASSWORD_PORTAL'),
        db_port=env('DB_PORT_PORTAL'),
    ),

)

