from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException,Request
from database import db,categoryCollection,offerBannerCollection,repositoyDefinationCollection,userRegistrationCollection
from model.banner import OfferBanner
from model.category import Category
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from model.fieldDefination import FieldDefination
from model.login import Login
from model.registration import Registration
from model.repository import RepositoyDefination
from typing import List
from fastapi.responses import JSONResponse
from model.saveFramework import SaveFrameworkObject

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
   message=await create_empty_collection(repositoyDefination.repositoryName)
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
    repositories = list(repositoyDefinationCollection.find())
    return convert_object_ids(repositories)

@app.delete("/api/delete-repository/{repositoryID}")
async def delete_repository(repositoryID: str):
    object_id = ObjectId(repositoryID)
    collection = repositoyDefinationCollection.find_one({"_id": object_id})  # ❌ no await
    if collection:
        repositoyDefinationCollection.delete_one({"_id": object_id})
        db.drop_collection(collection["repositoryName"])  # keep await if using Motor
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
        {"$set": {"fieldDefination": field_def_list}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Repository not found")

    return "fieldDefination updated successfully"

# single repository list
@app.get("/api/repository-list/{repositoryID}")
async def single_respository(repositoryID: str):
    object_id = ObjectId(repositoryID)
    record = repositoyDefinationCollection.find_one({"_id": object_id})
    if record:
        return convert_object_ids(record)
    else:
        raise HTTPException(status_code=404, detail="Repository not found")

# save Record
@app.post("/api/saveRecord")
async def save_record(saveFrameworkObject: SaveFrameworkObject):
    object_id = ObjectId(saveFrameworkObject.repositoryID)
    repositoyDefination:RepositoyDefination = repositoyDefinationCollection.find_one({"_id": object_id})
    if repositoyDefination:
         collection_name = repositoyDefination["repositoryName"]  # ✅ access as dict
         collection = db[collection_name]  # dynamic collection
         result = collection.insert_one(saveFrameworkObject.record)
         return {"id": str(result.inserted_id), "message": "Record added"}
    else:
        raise HTTPException(status_code=404, detail="Repository not found")
    

@app.get("/api/record/{repositoryID}")
async def get_record(repositoryID: str):
    object_id = ObjectId(repositoryID)

    repositoyDefination =  repositoyDefinationCollection.find_one({"_id": object_id})
    
    if not repositoyDefination:
        raise HTTPException(status_code=404, detail="Repository not found")

    collection_name = repositoyDefination["repositoryName"]
    collection = db[collection_name]

    # Correct way to fetch and return all records
    cursor = collection.find()
    records = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        records.append(doc)

    return records

# save Record
@app.post("/api/registration")
async def save_record(registration: Registration):
   registration_dict = registration.dict()  # 👈 Convert to dict
   result = userRegistrationCollection.insert_one(registration_dict)
   return {"id": str(result.inserted_id), "message": "user register created"}


@app.post("/api/login")
async def user_login(login: Login):
    login_dict = login.dict()  # 👈 Convert to dict

    # Find the user with matching email and password
    user = userRegistrationCollection.find_one({
        "$or": [
            {"email": login_dict["email"]},
            {"username": login_dict["email"]}
        ],
        "password": login_dict["password"]
    })

    if user:
        user["_id"] = str(user["_id"])
        return {"message": "Login successful", "user":user}
    else:
       return JSONResponse(
        status_code=200,
        content={"message": "Invalid email or password"}
    )
   
def convert_object_ids(doc):
    if isinstance(doc, list):
        return [convert_object_ids(i) for i in doc]
    elif isinstance(doc, dict):
        return {
            key: convert_object_ids(str(value)) if isinstance(value, ObjectId) else convert_object_ids(value)
            for key, value in doc.items()
        }
    else:
        return doc
    
@app.delete("/api/deleteRecord/{repositoryID}/{recordID}")
async def delete_record(repositoryID: str, recordID: str):
    try:
        repo_obj_id = ObjectId(repositoryID)
        record_obj_id = ObjectId(recordID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    # Get repository definition to determine collection
    repositoyDefination = repositoyDefinationCollection.find_one({"_id": repo_obj_id})
    if not repositoyDefination:
        raise HTTPException(status_code=404, detail="Repository not found")

    collection_name = repositoyDefination["repositoryName"]
    collection = db[collection_name]

    result = collection.delete_one({"_id": record_obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"message": "Record deleted successfully"}

@app.get("/api/singleRecord/{repositoryID}/{recordID}")
async def get_single_record(repositoryID: str, recordID: str):
    try:
        repo_obj_id = ObjectId(repositoryID)
        record_obj_id = ObjectId(recordID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    # Get repository definition to determine collection
    repositoyDefination = repositoyDefinationCollection.find_one({"_id": repo_obj_id})
    if not repositoyDefination:
        raise HTTPException(status_code=404, detail="Repository not found")

    collection_name = repositoyDefination["repositoryName"]
    collection = db[collection_name]

    record = collection.find_one({"_id": record_obj_id})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record["_id"] = str(record["_id"])  # Convert ObjectId to string
    return record


@app.post("/api/updateRecord/")
async def update_record(saveFrameworkObject: SaveFrameworkObject):
    try:
        repo_obj_id = ObjectId(saveFrameworkObject.repositoryID)
        record_obj_id = ObjectId(saveFrameworkObject.recordID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    # Fetch repository definition to get collection name
    repositoyDefination = repositoyDefinationCollection.find_one({"_id": repo_obj_id})
    if not repositoyDefination:
        raise HTTPException(status_code=404, detail="Repository not found")

    collection_name = repositoyDefination["repositoryName"]
    collection = db[collection_name]

    # Perform the update
    result = collection.update_one(
        {"_id": record_obj_id},
        {"$set": saveFrameworkObject.record}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"message": "Record updated successfully"}
