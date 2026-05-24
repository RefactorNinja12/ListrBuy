from pydantic import BaseModel
from datetime import datetime

class ShoppingListCreate(BaseModel):
    name: str

class ShoppingListResponse(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class ShoppingListUpdate(BaseModel):
    name: str

class ShoppingListRequest(BaseModel):
    id: int
    