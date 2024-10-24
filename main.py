from fastapi import FastAPI, HTTPException

from app.Kafka.KafkaProvider import KafkaProvider
from app.Provider.DbProvider import DbProvider


from app.WorkWithSignals import WorkWithSignals

app = FastAPI()
wws = WorkWithSignals().setSignals()

@app.get("/notify/producer")
def request_and_add_to_mongodb():
    for i in range(1,5):
        KafkaProvider.produce_kafka("hello from python","python")

# Эндпоинт для получения всех данных из MongoDB
@app.get("/get_items")
def get_items():
    data = DbProvider().get_NoFilerRepo().get_data()
    return {"Count": len(data), "items": data }

