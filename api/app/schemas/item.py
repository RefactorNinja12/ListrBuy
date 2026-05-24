from pydantic import BaseModel
from _datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    quantity: int = 1
    price: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    quantity: int 
    price: Optional[float]
    is_checked: bool
    shopping_list_id: int
    created_at: datetime
    total_price: float
    model_config = {"from_attributes": True}

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[float] = None
    is_checked: Optional[bool] = None