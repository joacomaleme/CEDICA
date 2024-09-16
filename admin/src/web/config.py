class Config(object):
    """Configuración Base"""

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Configuración de Producción"""
    pass

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    pass

class TestingConfig(Config):
    """Configuración de Testing"""
    TESTING = True
    pass

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}