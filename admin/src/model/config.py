from os import environ

class Config(object):
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "E2vrqJtoPWpwTdXZexa1"
    MINIO_SECRET_KEY = "lbr2NV57JVTCsyZYuwqwsaXWry2OiY7vv0kZv68v"
    MINIO_SECURE = False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "postgres"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class TestingConfig(Config):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
