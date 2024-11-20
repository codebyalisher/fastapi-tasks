#In FastAPI, function-based views are used directly by defining endpoint functions decorated with route decorators.
@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()
#FastAPI does not use class-based views directly (like DRF), but you can organize views using classes for more structure.
class ItemView:
    @app.get("/items/{item_id}")
    def get_item(self, item_id: int, db: Session = Depends(get_db)):
        return db.query(ItemDB).filter(ItemDB.id == item_id).first()
