from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

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