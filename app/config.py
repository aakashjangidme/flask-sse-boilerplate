import os

from app.database.database_client import DatabaseType


class Config:
    SECRET_KEY = '1234_SECRET_KEY'
    DATABASES = {
        DatabaseType.SQLITE.value: os.getenv("SQLITE_DATABASE_URL", "app.db"),
        DatabaseType.POSTGRES.value: os.getenv("PG_DATABASE_URL", "postgresql://x_pgdb:passw@localhost:5432/x_pgdb"),
        # DatabaseType.ORACLE.value: os.getenv("ORA_DATABASE_URL", "oracle://user:pass@localhost:1521/x_oradb")  # Uncomment when OracleClient is implemented
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
