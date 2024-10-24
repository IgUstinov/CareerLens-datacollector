from app.MongoDB.Conf.MongoDBSecret import MongoDBSecret


class NoFilterRepository(MongoDBSecret):
    def __init__(self,NoFilterDoc:str = "NoFilterDoc"):

        super().__init__()  # Инициализируем базовый класс
        self.collection = self.db[NoFilterDoc]  # Используем атрибут db из базового класса

    def post_data(self,data):
        result = self.collection.insert_many(data["items"])
        insertedIds = result.inserted_ids
        print(f"insertedIds count {len(insertedIds)}")
        ids = []

        for item in insertedIds:
            ids.append(str(item)) # Преобразование ObjectId в строку
        print(ids)
        return {"ids": ids}

    def get_data(self):
        items = list(self.collection.find())
        for item in items:
            item["_id"] = str(item["_id"])  # Преобразование ObjectId в строку
        return  items

    def add_item(self,item: dict):
        result = self.collection.insert_one(item)
        return {"status": "item added", "id": str(result.inserted_id)}