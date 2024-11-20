#Filtering, Search, Ordering:FastAPI integrates with libraries like SQLAlchemy and Filters to handle filtering, searching, and ordering.
from fastapi import Query

@app.get("/items/")
def list_items(sort_by: str = Query(None, alias="order_by")):
    if sort_by:
        return db.query(ItemDB).order_by(sort_by).all()
    return db.query(ItemDB).all()
