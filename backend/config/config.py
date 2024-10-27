from dynaconf import Dynaconf
from pathlib import Path
from loguru import logger

backend_config = Dynaconf(
    envvar_prefix="APP",
    settings_files=[
        Path(__file__).parent / ".secrets.toml",
        Path(__file__).parent / "settings.toml",
    ],
    environments=True,
    load_dotenv=True,
    environment="development"
)

backend_config.database_url = (
    f"postgresql+asyncpg://"
    f"{backend_config.database.username}:"
    f"{backend_config.database.password}@"
    f"{backend_config.database.host}:"
    f"{backend_config.database.port}/"
    f"{backend_config.database.name}"
)
