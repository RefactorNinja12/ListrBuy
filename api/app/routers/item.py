from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.auth import get_current_user
from app.services.item import ItemService

router = APIRouter(prefix="/item", tags=["item"])
item_service = ItemService()


@router.post("/create/{shopping_id}", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    request: ItemCreate,
    shopping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return item_service.create_item(db, shopping_id, current_user, request)

@router.get("/get-all/{shopping_id}", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
def get_all_item(
    shopping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return item_service.get_all(db, shopping_id, current_user)

@router.get("/{shoppinglist_id}/item/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_item_by_id(
    shoppinglist_id: int, 
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return item_service.get_by_id(db, shoppinglist_id, item_id, current_user)

@router.put("/{shoppinglist_id}/item/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def update_item(
    shoppinglist_id: int, 
    item_id: int, 
    request: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return item_service.update_item(db, shoppinglist_id, current_user, request, item_id)

@router.delete("/{shoppinglist_id}/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    shoppinglist_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item_service.delete_item(db, item_id, shoppinglist_id, current_user)