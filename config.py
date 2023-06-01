from functools import lru_cache

from pydantic import BaseSettings


@lru_cache()
def config():
    return Settings()


class Settings(BaseSettings):
    app_name: str
    db_host: str
    db_port: str
    db_database: str
    db_user: str
    db_password: str

    class Config:
        env_file = ".env"
