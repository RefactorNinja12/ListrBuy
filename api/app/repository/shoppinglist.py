from app.models.shoppinglist import ShoppingList
from sqlalchemy.orm import Session
from app.models.user import User
class ShoppingListRepository:

    def get_all(self, db: Session, user: User) -> list[ShoppingList]:
        return db.query(ShoppingList).filter(ShoppingList.user_id == user.id).all()
    def get_by_id(self, db:Session, id: int) -> ShoppingList:
        return db.query(ShoppingList).filter(ShoppingList.id == id).first()
    def create(self, db:Session, shoppinglist: ShoppingList) -> ShoppingList:
        db.add(shoppinglist)
        db.commit()
        db.refresh(shoppinglist)
        return shoppinglist
    def update(self, db: Session, shoppinglist: ShoppingList) -> ShoppingList: 
        db.commit()
        db.refresh(shoppinglist)
        return shoppinglist
    def delete(self, db: Session, shoppinglist: ShoppingList) -> None:
        db.delete(shoppinglist)
        db.commit()
