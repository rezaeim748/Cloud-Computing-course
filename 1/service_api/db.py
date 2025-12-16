from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env file")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    email = Column(String(255), nullable=False)
    state = Column(String(32), default="pending")  # pending | rejected | approved
    category = Column(String(128), nullable=True)
    image_key = Column(String(512), nullable=True)

def init_db():
    Base.metadata.create_all(engine)
