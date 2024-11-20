#CRUD API Using Function-Based Views:
#In FastAPI, you can use function-based views (like DRF function-based views).
@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(ItemDB).filter(ItemDB.id == item_id).first()
