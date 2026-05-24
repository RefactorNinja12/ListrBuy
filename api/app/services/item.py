from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.models.item import Item
from app.models.user import User
from app.repository.item import ItemRepository
from app.repository.shoppinglist import ShoppingListRepository

class ItemService:
    item_repo = ItemRepository()
    shopping_repo = ShoppingListRepository()


    def get_all(self, db: Session, shopping_id: int, user: User) -> list[ItemResponse]:
        shoppinglist = self.shopping_repo.get_by_id(db, shopping_id)
        if shoppinglist is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No shopping list with this id"
            )
        if shoppinglist.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        return self.item_repo.get_all(db, shoppinglist.id)
    
    
    def get_by_id(self, db: Session, shoppinglist_id: int, id: int, user: User) -> ItemResponse:
        shoppinglist = self.shopping_repo.get_by_id(db, shoppinglist_id)
        if shoppinglist is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="shopping list cant be found"
            )
        if shoppinglist.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        return self.item_repo.get_by_id(db, id, shoppinglist_id)
    
    def create_item(self, db: Session, shopping_id: int, user: User, request: ItemCreate) -> ItemResponse:
        shoppinglist = self.shopping_repo.get_by_id(db, shopping_id)

        if shoppinglist is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="shoppinglist not found"
            )
        if shoppinglist.user_id != user.id: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        new_item = Item(
            name = request.name,
            quantity = request.quantity,
            price = request.price,
            shopping_list_id = shoppinglist.id 
        )

        return self.item_repo.create(db, new_item)
    
    def update_item(self, db: Session, shopping_id: int, user: User, request: ItemUpdate, item_id: int) -> ItemResponse:
        shoppinglist = self.shopping_repo.get_by_id(db, shopping_id)
        if shoppinglist is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="shopping list not found"
            )
        if shoppinglist.user_id != user.id: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        
        item = self.item_repo.get_by_id(db, item_id, shoppinglist.id)
        if item is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="item not found"
            )
        item.name = request.name
        item.quantity = request.quantity
        item.price = request.price
        item.is_checked = request.is_checked
        return self.item_repo.update(db, item)
    
    def delete_item(self, db: Session, item_id: int, shopping_list_id: int, user: User) -> None: 
        shoppinglist = self.shopping_repo.get_by_id(db, shopping_list_id)
        if shoppinglist is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="shopping list not found"
            )
        if shoppinglist.user_id != user.id: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed"
            )
        item = self.item_repo.get_by_id(db, item_id, shopping_list_id)
        if item is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        self.item_repo.delete(db, item)


        