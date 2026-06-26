from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    fridge_items = relationship("FridgeItem", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class FridgeItem(Base):
    __tablename__ = "fridge_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, default=0)
    unit = Column(String, default="")
    category = Column(String, default="")
    expiry_date = Column(String, default="")

    user = relationship("User", back_populates="fridge_items")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(String, nullable=False)
    recipe_name = Column(String, nullable=False)
    recipe_image = Column(String, default="")

    user = relationship("User", back_populates="favorites")