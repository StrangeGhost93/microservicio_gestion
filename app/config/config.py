from asyncio.log import logger
from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Usar SQLite en memoria por defecto para tests si no hay variable definida
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///:memory:')
    
class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Usar SQLite local por defecto si no hay variable definida
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///sysacad.db')
        
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    # En producción, permitir definir por variable; fallback a SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI', 'sqlite:///sysacad_prod.db')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    
    return configuration.get(app, DevelopmentConfig)()