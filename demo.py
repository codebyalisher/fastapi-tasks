from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List
from model import User
from  fastapi import  FastAPI
from fastapi import HTTPException
import  asyncio
from bson import ObjectId  # To handle MongoDB _id fields
app=FastAPI()
client=None
users_collection=None

@app.on_event("startup")
async def startup():
    await init_db() 
    
@app.on_event("shutdown")
async def shutdown():
    if users_collection:
        client = users_collection.client  # Access the client through the collection
        client.close()
        print("MongoDB connection closed.")

# Function to initialize the database connection
async def init_db():
    global client,users_collection
    MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017/")# Default to localhost if not set
    if not MONGO_DETAILS:
        raise HTTPException(status_code=500, detail="MONGO_DETAILS environment variable is not set")
    try:
        client=AsyncIOMotorClient(MONGO_DETAILS)
        database = client.get_database("users")  # Use 'users' database
        users_collection = database.get_collection("user_collection")# Use 'user_collection'  
            
        print("MongoDB is connected and ready.")
    except Exception as e:
        print(f"an error occurred")
        users_collection=None


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "address": user.get("address", None),
    }

# Route to create a new user
@app.post("/users", response_model=dict)
async def create_user(user: User): 
    if users_collection is None:
        print("users_collection is not created",users_collection)
        raise HTTPException(status_code=500, detail="Database collection is not initialized")       
    user_dict = user.dict()  # Convert Pydantic model to dictionary
    new_user = await users_collection.insert_one(user_dict)  # Insert user into MongoDB
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})  # Retrieve the created user
    return user_helper(created_user)

# Route to get all users
@app.get("/users", response_model=List[dict])
async def get_users():
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

# Route to get a specific user by ID
@app.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)
async def main(): 
    await create_user()
    await get_users()
    await get_user()

if __name__ == '__main__':
    asyncio.run(main())
else:
    print("error: collection not created ")
