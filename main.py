from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException,Request
from database import db,categoryCollection,offerBannerCollection,repositoyDefinationCollection
from model.banner import OfferBanner
from model.category import Category
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from model.fieldDefination import FieldDefination
from model.repository import RepositoyDefination
from typing import List

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

# Allow all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

@app.delete("/api/categories/{category_id}")
async def delete_category(category_id: str):
    result = categoryCollection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")
    

@app.post("/api/uploadImage/")
async def upload_image(file: UploadFile = File(...)):
    folder = "images"
    os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
    original_filename = file.filename
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    new_filename = f"{name}_{timestamp}{ext}"
    file_location = os.path.join(folder, new_filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"fileurl": file_location, "message": "Image uploaded successfully"}

# banner slider
@app.post("/api/bannerOffer/")
async def create_banner_item(offerBanner: OfferBanner):
   offerBanner_dict = offerBanner.dict()  # 👈 Convert to dict
   result = offerBannerCollection.insert_one(offerBanner_dict)
   return {"id": str(result.inserted_id), "message": "Category created"}

@app.get("/api/bannerOffer/")
async def get_all_bannerOffer(request: Request):
    bannerOffer = []
    server_url = str(request.base_url)
    for item in offerBannerCollection.find():
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        item['ImageURL']=server_url +item["ImageURL"]
        bannerOffer.append(item)
    return bannerOffer

@app.delete("/api/bannerOffer/{bannerOffer_id}")
async def delete_category(bannerOffer_id: str):
    result = offerBannerCollection.delete_one({"_id": ObjectId(bannerOffer_id)})
    if result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")
    
# respository
@app.post("/api/repository")
async def create_repository(repositoyDefination: RepositoyDefination):
   repositoyDefination_dict = repositoyDefination.dict()  # 👈 Convert to dict
   result = repositoyDefinationCollection.insert_one(repositoyDefination_dict)
   message=await create_empty_collection(repositoyDefination.RepositoryName)
   return {"id": str(result.inserted_id), "message": message}

async def create_empty_collection(name: str):
    collections = db.list_collection_names()
    if name in collections:
        return f"Collection '{name}' already exists"

    db.create_collection(name)  # ✅ Sync call
    return f"Collection '{name}' created"

# GET: Fetch all categories
@app.get("/api/repository-list/")
async def get_all_repositories():
    repositories = []
    for item in repositoyDefinationCollection.find():
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        repositories.append(item)
    return repositories

@app.delete("/api/delete-repository/{repositoryID}")
async def delete_repository(repositoryID: str):
    object_id = ObjectId(repositoryID)
    collection = repositoyDefinationCollection.find_one({"_id": object_id})  # ❌ no await
    if collection:
        repositoyDefinationCollection.delete_one({"_id": object_id})
        db.drop_collection(collection["RepositoryName"])  # keep await if using Motor
        return {"message": "Repository deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Repository not found")
    
# field Defination
@app.post("/api/fieldDefination-update/{repositoryID}")
async def update_repository_defination(repositoryID: str, fieldDefination: List[FieldDefination]):
    # fieldDefination_dict = fieldDefination.dict()  # 👈 Convert to dict
    field_def_list = [f.dict() for f in fieldDefination]
    result =  repositoyDefinationCollection.update_one(
        {"_id": ObjectId(repositoryID)},
        {"$set": {"FieldDefination": field_def_list}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Repository not found")

    return "fieldDefination updated successfully"
