import logging
from app.MongoDB.Conf.MongoDBSecret import MongoDBSecret

logging.basicConfig(level=logging.INFO)


class NoFilterRepository(MongoDBSecret):
    def __init__(self, NoFilterDoc: str = "NoFilterDoc"):

        super().__init__()
        self.collection = self.db[NoFilterDoc]

    async def post_data(self, data):
        result = self.collection.insert_many(data)
        insertedIds = result.inserted_ids
        logging.info(f"insertedIds count {len(insertedIds)}")
        ids = []

        for item in insertedIds:
            ids.append(str(item))
        logging.info(ids)
        return {"ids": ids}

    async def get_data(self):
        items = list(self.collection.find())
        for item in items:
            item["_id"] = str(item["_id"])
        return items

    async def add_item(self, item: dict):
        result = self.collection.insert_one(item)
        return {"status": "item added", "id": str(result.inserted_id)}

    async def create_new_collection_with_filter(self, filter: dict):
        result = self.collection.insert_one(filter)
        return {"status": "item added", "id": str(result.inserted_id)}

    async def create_metadata(self, data):
        result = self.db["metadata"].insert_one(data)
        return result

    async def add_countries(self, data):
        result = self.db["countries"].insert_many(data)
        insertedIds = result.inserted_ids
        ids = []
        for item in insertedIds:
            ids.append(str(item))
        logging.info(ids)
        return {"ids": ids}
