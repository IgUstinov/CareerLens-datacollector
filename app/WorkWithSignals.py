import json
import logging
import uuid
from datetime import time

from app.CollectData.DataCollector import DataCollector
from app.Kafka.KafkaProvider import KafkaProvider
from app.Provider.DbProvider import DbProvider

logging.basicConfig(level=logging.INFO)
class WorkWithSignals:
    __dbProvider = DbProvider()


    def __init__(self,base_url):
        self.__collector = DataCollector(base_url)
        self.__kafkaProvider = KafkaProvider(self.__collector, self.__dbProvider,)

    async def start(self):
        logging.info("Запуск сбора данных")
        await self.__kafkaProvider.start_collecting_data("Backend")



