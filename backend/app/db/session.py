from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.db.base import Base

settings = get_settings()


def get_engine() -> Engine:
    """Create the SQLAlchemy engine for the active database backend."""

    database_url = settings.resolved_database_url
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

    return create_engine(
        database_url,
        connect_args=connect_args,
        echo=settings.sql_echo,
        future=True,
    )


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db_session() -> Generator[Session, None, None]:
    """Provide a database session for FastAPI dependencies."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def ensure_sqlite_columns() -> None:
    """Add new columns to the local SQLite database when the schema evolves."""

    if not settings.resolved_database_url.startswith("sqlite"):
        return

    inspector = inspect(engine)

    if "batting_stats" in inspector.get_table_names():
        batting_columns = {column["name"] for column in inspector.get_columns("batting_stats")}
        if "innings" not in batting_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE batting_stats ADD COLUMN innings INTEGER DEFAULT 0 NOT NULL"))

    if "bowling_stats" in inspector.get_table_names():
        bowling_columns = {column["name"] for column in inspector.get_columns("bowling_stats")}
        if "overs" not in bowling_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE bowling_stats ADD COLUMN overs NUMERIC DEFAULT 0 NOT NULL"))


def init_db() -> bool:
    """Create tables for the current metadata."""

    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_sqlite_columns()
    return True
