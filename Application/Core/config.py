from Application.Database.session import settings as db_settings

class Settings:
    DATABASE_URL = db_settings.DATABASE_WRITE_URL
    DATABASE_READ_URL = db_settings.DATABASE_READ_URL
    POSTGRES_USER = db_settings.POSTGRES_USER
    POSTGRES_PASSWORD = db_settings.POSTGRES_PASSWORD
    POSTGRES_DB = db_settings.POSTGRES_DB
    POSTGRES_HOST = db_settings.POSTGRES_HOST
    POSTGRES_PORT = db_settings.POSTGRES_PORT

settings = Settings()