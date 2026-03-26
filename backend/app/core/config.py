from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "CricAnalyzer API"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    frontend_origin: str = "http://localhost:3000"
    database_url: str = ""
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_db_url: str = ""
    auto_create_tables: bool = True
    sql_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def resolved_database_url(self) -> str:
        """Return the active database URL, defaulting to a local SQLite file."""

        if self.database_url:
            return self.database_url

        if self.supabase_db_url:
            return self.supabase_db_url

        sqlite_path = Path(__file__).resolve().parents[2] / "cricanalyzer.db"
        return f"sqlite:///{sqlite_path.as_posix()}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
