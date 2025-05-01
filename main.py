import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["user_service"]
users_collection = db["users"]

class User(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: User):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

@app.get("/users")
async def get_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fitness Tracker User Service!"}
