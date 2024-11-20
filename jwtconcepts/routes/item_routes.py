from fastapi import  File, UploadFile, APIRouter,HTTPException,FastAPI,Depends
from fastapi.responses import JSONResponse
from dependecies.jwt_login_logout import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc
from fastapi import Query
from fastapi import Depends
from models.itemdb import Item
from schemas.user_login_logout import ItemResponse,ItemCreate
    
router=APIRouter() 

# Function to create a new item
@router.post("/items/", response_model=ItemResponse)
def deserialization(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        print(item.name,item.description,item.price)
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



@router.get("/filter_order_search/",response_model=list[ItemResponse])
def filter_order_search(sort_by: str = Query(None, alias="order_by"), db: Session = Depends(get_db)):
    if sort_by:
        # Dynamically map 'sort_by' to an actual column (e.g., Itemdb.name)
        if sort_by == "name":
            return db.query(Itemdb).order_by(asc(Itemdb.name)).all()
        elif sort_by == "-name":
            return db.query(Itemdb).order_by(desc(Itemdb.name)).all()
        # Add other fields as needed
    return db.query(Itemdb).all()

#crud api using function-based views
@router.get("/items/{item_id}")
def crud_api_func(item_id: int, db: Session = Depends(get_db)):
    return db.query(Itemdb).filter(Itemdb.id == item_id).first()

#pagination 
@router.get("/items/")
def pagination(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Itemdb).offset(skip).limit(limit).all()
    return items

@router.get("/items/")
def function_base_view(db: Session = Depends(get_db)):
    return db.query(Itemdb).all()


#FastAPI does not use class-based views directly (like DRF), but you can organize views using classes for more structure.
class ItemView:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/items/{item_id}", self.get_item, methods=["GET"])

    @router.get("/items/{item_id}", operation_id="get_item_by_id")
    def get_item(self, item_id: int, db: Session = Depends(get_db)):
        return db.query(Itemdb).filter(Itemdb.id == item_id).first()


 
@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return JSONResponse(content={"filename": file.filename, "content_type": file.content_type})