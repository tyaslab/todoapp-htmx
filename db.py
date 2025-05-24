from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

engine = create_engine(config.DB)
Session = sessionmaker(bind=engine, expire_on_commit=False)
