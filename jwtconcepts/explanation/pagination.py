#Pagination:FastAPI uses offset pagination or limit/offset directly via query parameters.
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items
