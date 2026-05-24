from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base 
from sqlalchemy.orm import relationship

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="shopping_lists")
    items = relationship("Item", back_populates= "shopping_list", cascade="all, delete-orphan")
