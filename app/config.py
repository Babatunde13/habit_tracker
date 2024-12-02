import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://tracker:tracker@localhost:5432/tracker'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

env = os.environ.get('ENV', 'development')
config = DevelopmentConfig if env == 'development' else ProductionConfig
