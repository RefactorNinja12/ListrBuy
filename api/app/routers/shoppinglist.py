from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.shoppinglist import ShoppingListCreate, ShoppingListResponse, ShoppingListUpdate
from app.services.auth import get_current_user
from app.services.shoppinglist import ShoppingListService

router = APIRouter(prefix="/shoppinglist", tags=["shoppinglist"])
shoppinglist_service = ShoppingListService()


@router.post("/create", response_model=ShoppingListResponse, status_code=status.HTTP_201_CREATED)
def create_shoppinglist(
    request: ShoppingListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return shoppinglist_service.create_shoppinglist(db, request, current_user)

@router.get("/get-all", response_model=list[ShoppingListResponse], status_code=status.HTTP_200_OK)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return shoppinglist_service.get_all_shoppinglist(db, current_user)

@router.get("/{id}", response_model=ShoppingListResponse, status_code=status.HTTP_200_OK)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return shoppinglist_service.get_shoppinglist_by_id(db, id, current_user)

@router.put("/{id}", response_model=ShoppingListResponse, status_code=status.HTTP_200_OK)
def update_shoppinglist(
    id: int,
    request: ShoppingListUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return shoppinglist_service.update_shoppinglist(db, id, request, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shoppinglist(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    shoppinglist_service.delete_shoppinglist(db, id, current_user)
