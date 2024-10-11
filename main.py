from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from models import Item
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional
from fastapi.encoders import jsonable_encoder


app = FastAPI()

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.fastapi_db 



# 1
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    item_dict["insert_date"] = datetime.today() 
    result = await db["items"].insert_one(item_dict)
    return {"id": str(result.inserted_id)}



# 2
@app.get("/items/{id}")
async def get_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    item = await db["items"].find_one({"_id": ObjectId(id)})
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return jsonable_encoder(item, custom_encoder={ObjectId: str})

# 3
@app.get("/filter/items")
async def filter_items(email: Optional[str] = None, expiry_date: Optional[datetime] = None, 
                       insert_date: Optional[datetime] = None, quantity: Optional[int] = None):
    q = {}
    if email:
        q["email"] = email
    if expiry_date:
        q["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        q["insert_date"] = {"$gt": insert_date}
    if quantity:
        q["quantity"] = {"$gte": quantity}
    print("q==>",q)
    items = await db["items"].find(q).to_list(100)
    # return items
    pipeline = [
        {"$match": q}, 
        {"$group": {
            "_id": "$email",
            "count": {"$sum": 1}
        }}
    ]
    
    summary = await db["items"].aggregate(pipeline).to_list(100)
    return {
        "items": jsonable_encoder(items, custom_encoder={ObjectId: str}),
        "summary": jsonable_encoder(summary, custom_encoder={ObjectId: str}),
    }

# 4
@app.delete("/items/{id}")
async def delete_item(id: str):
    print("id===>",id)
    result = await db["items"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


# 5
@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    item_dict = item.dict(exclude_unset=True)
    result = await db["items"].update_one({"_id": ObjectId(id)}, {"$set": item_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found or no changes made")
    return {"message": "Item updated"}

# ==== User Clock-In Records APIs ==========

# 6
@app.post("/clock-in")
async def create_clock_in(email: str = Body(...), location: str = Body(...)):
    clock_in_data = {
        "email": email,
        "location": location,
        "insert_datetime": datetime.today()  
    }
    result = await db["clock_in_records"].insert_one(clock_in_data)
    
    return {"id": str(result.inserted_id), "message": "Clock-in entry created successfully"}

# 7
@app.get("/clock-in/{id}")
async def get_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID")
    
    clock_in_record = await db["clock_in_records"].find_one({"_id": ObjectId(id)})
    
    if not clock_in_record:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    
    clock_in_record["_id"] = str(clock_in_record["_id"]) 
    return clock_in_record

# 8
@app.get("/filter/clock-in")
async def filter_clock_in_records(
    email: Optional[str] = None, 
    location: Optional[str] = None, 
    insert_datetime: Optional[datetime] = None
):
    q = {}

    if email:
        q["email"] = email
    if location:
        q["location"] = location
    if insert_datetime:
        q["insert_datetime"] = {"$gt": insert_datetime}

    clock_in_records = await db["clock_in_records"].find(q).to_list(100)

    for record in clock_in_records:
        record["_id"] = str(record["_id"])  
    
    return clock_in_records

# 9
@app.delete("/clock-in/{id}")
async def delete_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID")
    
    delete_result = await db["clock_in_records"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    
    return {"message": "Clock-in record deleted successfully"}

# 10
@app.put("/clock-in/{id}")
async def update_clock_in(id: str, email: Optional[str] = Body(None), location: Optional[str] = Body(None)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid clock-in ID")
    
    update_data = {}
    if email:
        update_data["email"] = email
    if location:
        update_data["location"] = location

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_result = await db["clock_in_records"].update_one(
        {"_id": ObjectId(id)}, 
        {"$set": update_data}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Clock-in record not found or no changes made")
    
    return {"message": "Clock-in record updated successfully"}