from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database and create tables."""
    from app import models
    models.Base.metadata.create_all(bind=engine)
