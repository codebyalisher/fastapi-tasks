from typing import Union,Optional,List
from pydantic import BaseModel
from fastapi import FastAPI,Query,Depends

app = FastAPI()


class User(BaseModel):
    name: str
    password: int  # Assuming password is a string
    address: Optional[str] = Query(None,max_length=5,regex="al")#bascally query is used to validate the values
@app.get("/")
def read_root():
    return {"Hello": "World this is the alisher"}


@app.get("/items/{item_id}")#here there is a query parameters
def read_item(item_id: int, q: Union[List[str]]=Query(['foo','ni'])):#here we are passing as a optional parameters which is union and its value is none initially
    return {"item_id": item_id, "q": q}

@app.get("/filepath/{file_path:path}")#here we are passing the path of the file,here flow is that we are getting value from path and passing into the function to send the reponse tot he user
def filepath(file_path:str):
    return {"filepath": file_path}

@app.put("/items")#remember whenever we have to ue the put,post or update methods we have to first create the models and store the data in it from req.body or passing the values in models variabeles from the browser and after validation show them
def fetchdata(user: User):#validataion can be done using query
        return {
        "name": user.name,
        "password": user.password,
        "optional address": user.address
    }

#dependcy injection using fucntions but we can also do the same with the classes, also anything whcih is callable is called dpendency
async def common_param(q:Optional[str]=None,skip:int=0,limit:int=10):
    return {'q':q,'skip':skip,'limit':limit}

@app.get('/items')
async def read_items(common:dict=Depends(common_param)):
    return common
@app.get('/users')#here in the above function logic have same shared
async def read_items(common:dict=Depends(common_param)):
    return common

#dependency using class
class CommonParams:
    def __init__(self,q:Optional[int]=10,skip:int=0,limit:int=0):
        self.q=q 
        self.skip=skip 
        self.limit=limit
@app.get('/readitems')
async def read_items(common:CommonParams=Depends(CommonParams)):
    res={}
    return common.q+common.skip+common.limit