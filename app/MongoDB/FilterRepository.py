import logging
from app.MongoDB.Conf.MongoDBSecret import MongoDBSecret
logging.basicConfig(level=logging.INFO)

class FilterRepository(MongoDBSecret):
    def __init__(self,FilterDoc:str = "FilterDoc"):

        super().__init__()
        self.collection = self.db[FilterDoc]


    async def create_metadata(self, metadata):
        self.db["metadata_collection"].insert_one(metadata)

    async def create_new_collection_with_filter(self, collection_name, filtered_data: dict):
        new_collection = self.db[collection_name]
        new_collection.insert_many(filtered_data)
        logging.info(f"Отфильтрованные данные сохранены в коллекцию: {collection_name}")

    async def find_data(self,mongo_filter):
        # Выполняем запрос к MongoDB с фильтрацией
        NoFileredCollection = self.db["NoFilterDoc"]
        logging.info(mongo_filter)
        filtered_data = list(NoFileredCollection.find(mongo_filter))
        logging.info(filtered_data)
        return filtered_data
