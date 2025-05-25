from typing import Union
from fastapi import FastAPI, File, UploadFile
from database import categoryCollection
from model.category import Category
import shutil
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World222"}

@app.post("/api/categories/")
async def create_item(category: Category):
   category_dict = category.dict()  # 👈 Convert to dict
   result = categoryCollection.insert_one(category_dict)
   return {"id": str(result.inserted_id), "message": "Category created"}

# GET: Fetch all categories
@app.get("/api/categories/")
async def get_all_categories():
    categories = []
    for item in categoryCollection.find():
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        categories.append(item)
    return categories

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    folder = "images"
    os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
    file_location = f"images/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"fileurl": file_location, "message": "Image uploaded successfully"}