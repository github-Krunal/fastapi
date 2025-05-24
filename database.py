from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import MongoClient

MONGO_DETAILS = "mongodb://localhost:27017"

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client["codeInnovator"]
categoryCollection = db["category"]
