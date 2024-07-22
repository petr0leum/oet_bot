import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание каталога для базы данных, если он не существует
db_path = os.path.join(os.path.dirname(__file__), "data", "db")
if not os.path.exists(db_path):
    os.makedirs(db_path)

DATABASE_URL = f"sqlite:///{os.path.join(db_path, 'user_cards.db')}"

# Create the engine and the session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    card_data = Column(Text)

# Create the tables
Base.metadata.create_all(bind=engine)

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

def get_last_five_user_cards(user_id: str):
    """Get the last five saved cards for the user"""
    db = next(get_db())
    user_cards = db.query(UserCard).filter(UserCard.user_id == user_id).order_by(UserCard.id.desc()).limit(5).all()
    db.close()
    return user_cards
