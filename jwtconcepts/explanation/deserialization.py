#Deserialization and Insert Data:
#FastAPI automatically performs deserialization when you accept request bodies in the form of Pydantic models. To insert data into a database, you would typically use an ORM like SQLAlchemy.
from fastapi import Depends
from sqlalchemy.orm import Session

# Assume you have a SQLAlchemy session and model
@app.post("/items/")
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    return db_item
