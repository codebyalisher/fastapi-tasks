from fastapi import FastAPI, HTTPException
from typing import List
from model import User  # Import the Pydantic User model
from mongo import Database  # Import from db.py
from bson import ObjectId
import asyncio


app=FastAPI()
db=Database()
# Initialize MongoDB connection at startup
@app.on_event("startup")
async def startup():
    print("Starting MongoDB initialization...")  # Debug log for startup
    await db.init_db()  # Initialize the database connection
    print("MongoDB initialization complete.")  # Initialize the database connection  
@app.on_event("shutdown")
async def shutdown():
    if db.users_collection:
        client = db.users_collection.client  # Access the client through the collection
        client.close()
        print("MongoDB connection closed.")


# Helper function to convert MongoDB document to a dict
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
    if db.users_collection is None:
        print("users_collection is not created",db.users_collection)
        raise HTTPException(status_code=500, detail="Database collection is not initialized")       
    user_dict = user.dict()  # Convert Pydantic model to dictionary
    new_user = await db.users_collection.insert_one(user_dict)  # Insert user into MongoDB
    created_user = await db.users_collection.find_one({"_id": new_user.inserted_id})  # Retrieve the created user
    return user_helper(created_user)

# Route to get all users
@app.get("/users", response_model=List[dict])
async def get_users():
    users = []
    async for user in db.users_collection.find():
        users.append(user_helper(user))
    return users

# Route to get a specific user by ID
@app.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: str):
    user = await db.users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

#updating the user record
@app.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User):
    existing_user = await db.users_collection.find_one({"_id": ObjectId(user_id)})    
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Update only the fields passed in the request body
    updated_data = user.dict(exclude_unset=True)    
    # Update the user in the database
    update_result = await db.users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_data}
    )
    # Check if any document was updated
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    # Retrieve the updated user document
    updated_user = await db.users_collection.find_one({"_id": ObjectId(user_id)})    
    return user_helper(updated_user)

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    user = await db.users_collection.find_one({"_id": ObjectId(user_id)})    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")    
    # Perform the deletion
    delete_result = await db.users_collection.delete_one({"_id": ObjectId(user_id)})    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    # Return the deleted user data
    return {"message": "User deleted successfully", "user": user_helper(user)}

async def main(): 
    await create_user()
    await get_users()
    await get_user()
    await update_user()
    await delete_users()

if __name__ == '__main__':
    asyncio.run(main())
else:
    print("error: collection not created ")
