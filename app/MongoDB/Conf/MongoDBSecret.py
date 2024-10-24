from pymongo import MongoClient

class MongoDBSecret:
    def __init__(self):
        self.mongo_client = MongoClient("mongodb://mongodb:27017/")
        self.db = self.mongo_client["career_lens"]
