from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Application.Database.base import Base
class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    unit = Column(String(50))

    recipe_links = relationship("RecipeIngredient", back_populates="ingredient")
    user_links = relationship("UserIngredient", back_populates="ingredient")