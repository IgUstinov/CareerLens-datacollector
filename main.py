from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

from app.CollectData.Collector import get_it_vacancies

app = FastAPI()

# Подключение к MongoDB
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["career_lens"]
collection = db["NoFilterDoc"]



@app.get("/notify/")
def send_data():
    data = get_it_vacancies()
    print(data)
    result = collection.insert_many(data["items"])
    return {"status": "data sent"}

# Эндпоинт для добавления данных в MongoDB
@app.post("/add-item/")
def add_item(item: dict):
    result = collection.insert_one(item)
    return {"status": "item added", "id": str(result.inserted_id)}

# Эндпоинт для получения всех данных из MongoDB
@app.get("/get-items/")
def get_items():
    items = list(collection.find())
    for item in items:
        item["_id"] = str(item["_id"])  # Преобразование ObjectId в строку
    return {"Count": len(items), "items": items }
