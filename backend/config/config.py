from pathlib import Path

from dynaconf import Dynaconf
from loguru import logger
from pydantic import BaseModel, Field, HttpUrl


class DatabaseConfig(BaseModel):
    port: int = Field(..., json_schema_extra={"example": 5432})
    name: str = Field(..., json_schema_extra={"example": "schedule"})
    host: str = Field(..., json_schema_extra={"example": "localhost"})
    username: str = Field(..., json_schema_extra={"example": "user"})
    password: str = Field(..., json_schema_extra={"example": "pass"})
    url: str = Field(..., json_schema_extra={"example": "driver://user:pass@localhost/dbname"})


class ParsingConfig(BaseModel):
    interval: int = 3600
    retry_attempts: int = 3
    retry_delay: int = 300
    chunk_size: int = 20
    chunk_delay: float = 1.0
    concurrent_requests: int = 15


class SourceConfig(BaseModel):
    schedule_url: HttpUrl = Field(..., json_schema_extra={"example": "https://mai.ru/education/studies/schedule/index.php"})
    groups_url: HttpUrl = Field(..., json_schema_extra={"example": "https://public.mai.ru/schedule/data/groups.json"})
    api_url: HttpUrl = Field(..., json_schema_extra={"example": "https://public.mai.ru/schedule/data"})



_config = Dynaconf(
    envvar_prefix="APP",
    settings_files=[
        Path(__file__).parent.parent / ".secrets.toml",
        Path(__file__).parent.parent / "config.toml",
    ],
    environments=True,
    load_dotenv=True,
    environment="development",
)

database_config = DatabaseConfig(
    port=_config.database.port,
    name=_config.database.name,
    host=_config.database.host,
    username=_config.database.username,
    password=_config.database.password,
    url=f"postgresql+asyncpg://{_config.database.username}:{_config.database.password}@"
        f"{_config.database.host}:{_config.database.port}/{_config.database.name}"
)

test_database_config = DatabaseConfig(
    port=_config.test_database.port,
    name=_config.test_database.name,
    host=_config.test_database.host,
    username=_config.test_database.username,
    password=_config.test_database.password,
    url=f"postgresql+asyncpg://{_config.test_database.username}:{_config.test_database.password}@"
        f"{_config.test_database.host}:{_config.test_database.port}/{_config.test_database.name}"
)

parsing_config = ParsingConfig(
    interval=_config.parsing.interval,
    retry_attempts=_config.parsing.retry_attempts,
    retry_delay=_config.parsing.retry_delay,
    chunk_size=_config.parsing.chunk_size,
    chunk_delay=_config.parsing.chunk_delay,
    concurrent_requests=_config.parsing.concurrent_requests,
)

source_config = SourceConfig(
    schedule_url=_config.source.schedule_url,
    groups_url=_config.source.groups_url,
    api_url=_config.source.api_url,
)
