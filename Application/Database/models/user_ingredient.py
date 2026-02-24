from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from Application.Database.base import Base
class UserIngredient(Base):
    __tablename__ = "user_ingredients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "ingredient_id"),
    )

    user = relationship("User", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="user_links")