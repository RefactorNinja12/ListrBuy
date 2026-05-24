from sqlalchemy.orm import Session
from app.models.item import Item



class ItemRepository:


    def get_all(self, db: Session, id: int) -> list[Item]: 
        return db.query(Item).filter(Item.shopping_list_id == id).all()
    

    def get_by_id(self, db: Session, id: int, shoppinglist_id: int) -> Item: 
        return db.query(Item).filter(Item.id == id, Item.shopping_list_id == shoppinglist_id).first()
    

    def update(self, db: Session, item: Item) -> Item: 
        db.commit()
        db.refresh(item)
        return item
    

    def create(self, db: Session, item: Item) -> Item:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    

    def delete(self, db: Session, item: Item) -> None: 
        db.delete(item)
        db.commit()