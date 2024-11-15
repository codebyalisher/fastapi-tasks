from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import HTTPException

# Function to initialize the database connection
class Database:
    def __init__(self):
        self.client = None
        self.database = None
        self.users_collection = None
    async def init_db(self):     
        MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017/")# Default to localhost if not set
        if not MONGO_DETAILS:
            raise HTTPException(status_code=500, detail="MONGO_DETAILS environment variable is not set")
        try:
            self.client=AsyncIOMotorClient(MONGO_DETAILS)
            self.database = self.client.get_database("users")  # Use 'users' database
            self.users_collection = self.database.get_collection("user_collection")# Use 'user_collection'                        
            if self.users_collection is None:
                print("users_collection is still None!")  # Debug log if collection is not created
            else:
                print("MongoDB connected successfully and users_collection initialized.")      
        except Exception as e:
            print(f"an error occurred")
            raise HTTPException(status_code=500, detail="Database connection failed")





