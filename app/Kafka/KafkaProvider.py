import json
import logging
import time
import uuid

from app.CollectData.DataCollector import DataCollector
from app.Kafka.Config.ConsumerKafka import ConsumerKafka
from app.Kafka.Config.ProducerKafka import ProducerKafka
from app.Provider.DbProvider import DbProvider


class KafkaProvider:

    def __init__(self, collector: DataCollector, dbProvider: DbProvider):
        self.dbProvider = dbProvider
        self.collector = collector

    async def produce_kafka(self, message, topic):
        ProducerKafka().deliver_message(message, topic)

    async def start_collecting_data(self, topic: str):
        consumer = ConsumerKafka(self.dbProvider, self.collector)
        async for msg in consumer.start(topic):
            try:
                logging.info(f"Обработка сообщения: {msg}")
                await self.got_message_from_backend(json.loads(msg.value))  # Логика обработки сообщения
            except Exception as ex:
                logging.error(ex)

    async def got_message_from_backend(self, msg):
        logging.info(f"collectData {msg}")
        if msg.get('collectData'):
            await self.start_collect_data(msg)
        if msg.get("filterData"):
            await self.process_message(msg)
        if msg.get("addCountries"):
            await self.CountryRequest(msg)

    async def start_collect_data(self, msg):
        logging.info("Start collect data from hh ru")
        collectData = msg.get('collectData')
        requestsId = msg.get('requestsId')
        async for batch in self.collector.get_vacancies_batches(collectData['count']):
            result = await self.dbProvider.get_NoFilerRepo().post_data(batch)
            logging.info("Add data: ", result)
            logging.info(result.items())
            added = {"Ids": result, "requestsId":requestsId}
            await self.added_data_to_mongodb(added)

    async def added_data_to_mongodb(self, ids):
        producer = ProducerKafka()
        await producer.deliver_message(ids, "Python")

    async def process_message(self, message):
        try:
            # Преобразуем сообщение из Kafka в JSON
            filter_data = message.get("filterData", {})
            request_id = message.get("requestId")  # Предполагаем, что requestId приходит с запросом

            mongo_filter = await self.flatten_dict(filter_data)
            logging.info(mongo_filter)
            # Генерация уникального имени коллекции
            timestamp = int(time.time() * 1000)  # метка времени в миллисекундах
            unique_id = uuid.uuid4().hex[:8]  # сокращенный UUID
            new_collection_name = f"filtered_data_{timestamp}_{unique_id}"

            # Фильтрация данных и сохранение в новую коллекцию
            filtered_data = await (self.dbProvider.get_FilterRepo()).find_data(mongo_filter)
            if filtered_data:
                await self.dbProvider.get_FilterRepo().create_new_collection_with_filter(new_collection_name,
                                                                                         filtered_data)
                # Сохраняем метаданные коллекции
                metadata = {
                    "request_id": request_id,
                    "timestamp": timestamp,
                    "filter_data": filter_data,
                    "collection_name": new_collection_name
                }
                await self.dbProvider.get_NoFilerRepo().create_metadata(metadata)

                # Отправляем имя коллекции в Kafka как ответ
                response = {"collectionName": new_collection_name, "request_id": request_id}
                logging.info(response)
                producer = ProducerKafka()
                await producer.deliver_message(json.dumps(response), "Python")
            else:
                logging.info("Нет данных, соответствующих фильтру.")
        except Exception as e:
            logging.info(f"Ошибка обработки сообщения: {e}")

    async def flatten_dict(self, data, parent_key='', separator='.'):
        items = {}
        for k, v in data.items():
            new_key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(await self.flatten_dict(v, new_key, separator=separator))
            else:
                items[new_key] = v
        return items

    async def CountryRequest(self, msg):
        requestsId = msg.get('requestsId')
        Countries = await self.collector.get_countries()
        result = await self.dbProvider.get_NoFilerRepo().add_countries(Countries)
        logging.info("Add data: ", result)
        await self.added_data_to_mongodb({"Ids": result, "requestsId": requestsId})
