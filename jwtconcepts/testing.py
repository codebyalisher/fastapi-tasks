from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from fastapi_sqlalchemy import DBSessionMiddleware

# Database setup
DATABASE_URL = "sqlite:///./your_database.db"  # Use a relative path for local dev

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for models
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

# Create tables (if they don't exist)
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

# FastAPI app setup
app = FastAPI()

# Add DB session middleware with the database URL
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

@app.on_event("startup")
async def startup():
    create_tables()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for input/output validation
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True

# Function to create a new item
def create_item(item: ItemCreate, db: Session):
    try:
        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding the item: {e}")

# Route to create a new item
@app.post("/items/", response_model=ItemResponse)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(item, db)
