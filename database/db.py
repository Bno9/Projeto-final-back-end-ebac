
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

engine = create_engine(
    DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)