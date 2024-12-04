import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://tracker:tracker@localhost:5432/tracker'
    TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or 'postgresql://tracker:tracker@localhost:5432/tracker_test'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class TestConfig(Config):
    TESTING = True
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or 'postgresql://tracker:tracker@localhost:5432/tracker_test'
    DEBUG = True

env = os.environ.get('ENV', 'development')

configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}

config = configs[env]() or DevelopmentConfig()
