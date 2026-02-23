from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    #created_at = Column(DateTime, default=datetime.utcnow)

    ingredients = relationship("UserIngredient", back_populates="user")
    favorites = relationship("UserFavorite", back_populates="user")
    recipes = relationship("Recipe", back_populates="author")