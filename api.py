from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World this is the alisher"}


@app.get("/items/{item_id}")#here there is a query parameters
def read_item(item_id: int, q: Union[str,None]=None):#here we are passing as a optional parameters which is union and its value is none initially
    return {"item_id": item_id, "q": q}

@app.get("/filepath/{file_path:path}")#here we are passing the path of the file,here flow is that we are getting value from path and passing into the function to send the reponse tot he user
def filepath(file_path:str):
    return {"filepath": file_path}