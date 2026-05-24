from sqlalchemy.orm import Session
from app.repository.shoppinglist import ShoppingListRepository
from app.schemas.shoppinglist import ShoppingListUpdate, ShoppingListCreate, ShoppingListResponse
from app.models.shoppinglist import ShoppingList
from fastapi import HTTPException, status
from app.models.user import User


class ShoppingListService:
    shopping_repo = ShoppingListRepository()

    def get_all_shoppinglist(self, db: Session, user: User) -> list[ShoppingListResponse]:
        return self.shopping_repo.get_all(db, user)

    def get_shoppinglist_by_id(self, db: Session, id: int, user: User) -> ShoppingListResponse:
        shopping_list = self.shopping_repo.get_by_id(db, id)
        if shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No shopping list with that id found"
            )
        if shopping_list.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        return shopping_list

    def create_shoppinglist(self, db: Session, request: ShoppingListCreate, user: User) -> ShoppingListResponse:
        new_list = ShoppingList(name=request.name, user_id=user.id)
        return self.shopping_repo.create(db, new_list)

    def update_shoppinglist(self, db: Session, id: int, update: ShoppingListUpdate, user: User) -> ShoppingListResponse:
        shopping_list = self.shopping_repo.get_by_id(db, id)
        if shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shopping list not found"
            )
        if shopping_list.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        shopping_list.name = update.name
        return self.shopping_repo.update(db, shopping_list)

    def delete_shoppinglist(self, db: Session, shopping_id: int, user: User) -> None:
        shopping_list = self.shopping_repo.get_by_id(db, shopping_id)
        if shopping_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shopping list not found"
            )
        if shopping_list.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        self.shopping_repo.delete(db, shopping_list)
