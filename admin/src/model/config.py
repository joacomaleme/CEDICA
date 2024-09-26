class Config(object):
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = None

class DevelopmentConfig(Config):
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
