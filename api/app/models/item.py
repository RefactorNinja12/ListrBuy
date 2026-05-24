from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Item(Base): 
    __tablename__ = "items"

    id= Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=True)
    is_checked = Column(Boolean, nullable=False, default=False)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shopping_list = relationship("ShoppingList", back_populates="items")
    @property
    def total_price(self) -> float:
        return (self.quantity or 0) * (self.price or 0)