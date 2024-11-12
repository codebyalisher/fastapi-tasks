from typing import Union,Optional
from pydantic import BaseModel
from fastapi import FastAPI,Query

app = FastAPI()


class User(BaseModel):
    name: str
    password: int  # Assuming password is a string
    address: Optional[str] = Query(None,max_length=5)#bascally query is used to validate the values
@app.get("/")
def read_root():
    return {"Hello": "World this is the alisher"}


@app.get("/items/{item_id}")#here there is a query parameters
def read_item(item_id: int, q: Union[str,None]=None):#here we are passing as a optional parameters which is union and its value is none initially
    return {"item_id": item_id, "q": q}

@app.get("/filepath/{file_path:path}")#here we are passing the path of the file,here flow is that we are getting value from path and passing into the function to send the reponse tot he user
def filepath(file_path:str):
    return {"filepath": file_path}

@app.put("/items")
def fetchdata(user: User):#validataion can be done using query
        return {
        "name": user.name,
        "password": user.password,
        "optional address": user.address
    }

    