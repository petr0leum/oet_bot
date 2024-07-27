import os
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

from config import settings


db_path = os.path.join(os.path.dirname(__file__), "data", "db")
if not os.path.exists(db_path):
    os.makedirs(db_path)

DATABASE_URL = f"sqlite:///{os.path.join(db_path, 'user_cards.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(String, index=True)
    card_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine) # Create the tables

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_user_card(user_id: str, card_data: str):
    """Save user's card to the database"""
    db = next(get_db())
    user_card = UserCard(user_id=user_id, card_data=card_data)
    db.add(user_card)
    db.commit()
    db.refresh(user_card)
    db.close()

def get_card_by_id(user_id: str, card_id: str):
    db = next(get_db())
    card = db.query(UserCard)\
        .filter(UserCard.user_id == user_id, UserCard.card_id == card_id)\
        .first()
    db.close()
    return card

def get_last_user_cards(user_id: str):
    """Get the last five saved cards for the user"""
    db = next(get_db())
    user_cards = db.query(UserCard)\
        .filter(UserCard.user_id == user_id)\
        .order_by(UserCard.created_at.desc())\
        .limit(settings.card_examples_num)\
        .all()
    db.close() 
    return user_cards

def get_last_user_card_ids(user_id: str, limit: int = settings.card_examples_num):
    """Get the IDs of the last saved cards for the user."""
    db = next(get_db())
    card_ids = (
        db.query(UserCard.card_id)
        .filter(UserCard.user_id == user_id)
        .order_by(UserCard.created_at.desc())
        .limit(limit)
        .all()
    )
    db.close()
    return [card.card_id for card in card_ids] if card_ids else []
