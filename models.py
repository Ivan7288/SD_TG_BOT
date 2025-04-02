from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class GeneratedImage(Base):
    __tablename__ = 'generated_images'
    
    id = Column(Integer, primary_key=True)
    prompt = Column(String(500))
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer)

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine) 