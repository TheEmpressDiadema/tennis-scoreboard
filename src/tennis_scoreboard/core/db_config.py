import tomllib

from typing import Any
from sqlalchemy import URL


class DBConfig:

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_DRIVER: str
    DB_PASSWORD: str
    DB_USER: str

    @classmethod
    def _write_config(cls, config: dict[str, Any]) -> None:
        cls.DB_HOST = config['host']
        cls.DB_PORT = config['port']
        cls.DB_NAME = config['database']
        cls.DB_DRIVER = config['driver']
        cls.DB_PASSWORD = config['password']
        cls.DB_USER = config['user']

    @classmethod
    def _get_db_config(cls, path: str) -> dict[str, Any]:
        with open(path, 'rb') as config_file:
            return tomllib.load(config_file)['mysql']

    @classmethod
    def get_database_url(cls, config_file: str, security_file: str) -> str:
        config = cls._get_db_config(config_file)
        config.update(cls._get_db_config(security_file))
        cls._write_config(config)
        return URL.create(
                drivername=config['driver'],
                username=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port'],
                database=config['database']
            ).render_as_string(hide_password=False)