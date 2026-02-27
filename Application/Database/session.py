import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    POSTGRES_HOST: str = "db"
    POSTGRES_REPLICA_HOST: str = "db-replica" 
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_WRITE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_READ_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_REPLICA_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    )


settings = Settings()

engine_write = create_engine(
    settings.DATABASE_WRITE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

engine_read = create_engine(
    settings.DATABASE_READ_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionWrite = sessionmaker(autocommit=False, autoflush=False, bind=engine_write)
SessionRead = sessionmaker(autocommit=False, autoflush=False, bind=engine_read)

def create_engine_with_retry(retries: int = 15, delay: int = 2):
    for attempt in range(1, retries + 1):
        try:
            engine = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True
            )
            with engine.connect():
                pass
            return engine
        except OperationalError:
            time.sleep(delay)

    raise Exception("Could not connect to database")


engine = create_engine_with_retry()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """Use for POST, PUT, DELETE (Write operations)"""
    db = SessionWrite()
    try:
        yield db
    finally:
        db.close()

def get_read_db():
    """Use for GET (Read operations)"""
    db = SessionRead()
    try:
        yield db
    finally:
        db.close()
        
engine = engine_write