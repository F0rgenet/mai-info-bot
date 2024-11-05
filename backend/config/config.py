from pathlib import Path

from dynaconf import Dynaconf
from pydantic import BaseModel, Field, HttpUrl


class DatabaseConfig(BaseModel):
    port: int = Field(..., example=5432)
    name: str = Field(..., example="schedule")
    host: str = Field(..., example="localhost")
    username: str = Field(..., example="user")
    password: str = Field(..., example="pass")
    url: str = Field(..., example="driver://user:pass@localhost/dbname")


class ParsingConfig(BaseModel):
    interval: int = 3600
    retry_attempts: int = 3
    retry_delay: int = 300
    chunk_size: int = 20
    chunk_delay: float = 1.0
    concurrent_requests: int = 15


class SourceConfig(BaseModel):
    schedule_url: HttpUrl = Field(..., example="https://mai.ru/education/studies/schedule/index.php")
    groups_url: HttpUrl = Field(..., example="https://public.mai.ru/schedule/data/groups.json")
    api_url: HttpUrl = Field(..., example="https://public.mai.ru/schedule/data")


_config = Dynaconf(
    envvar_prefix="APP",
    settings_files=[
        Path(__file__).parent / ".secrets.toml",
        Path(__file__).parent / "settings.toml",
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
