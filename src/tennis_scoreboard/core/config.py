import tomllib

from typing import Any
from sqlalchemy import URL

class DBConfig:

    _CONFIG_FILE = "db_config.toml"
    _SECURITY_FILE = "db_security.toml"

    @classmethod
    def _get_db_config(cls, path: str) -> dict[str, Any]:
        with open(path, 'rb') as config_file:
            return tomllib.load(config_file)['mysql']

    @classmethod
    def get_database_url(cls) -> str:
        config = cls._get_db_config(cls._CONFIG_FILE)
        config.update(cls._get_db_config(cls._SECURITY_FILE))
        return URL.create(
                drivername=config['driver'],
                username=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port'],
                database=config['database']
            ).render_as_string(hide_password=False)