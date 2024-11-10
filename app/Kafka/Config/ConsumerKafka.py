import logging
from aiokafka import AIOKafkaConsumer
from app.CollectData.DataCollector import DataCollector
from app.Provider.DbProvider import DbProvider

logging.basicConfig(level=logging.INFO)


class ConsumerKafka:
    def __init__(self, dbProvider: DbProvider, collector: DataCollector):
        self.consumer = AIOKafkaConsumer(
            "Backend",
            bootstrap_servers="kafka:9092",
            group_id="fastapi-group",
            auto_offset_reset="earliest"
        )
        self.dbProvider = dbProvider
        self.collector = collector

    async def start(self, topic: str):
        logging.info("Start consume")
        await self.consumer.start()
        try:
            async for msg in self.consumer:  # Цикл ожидания и обработки сообщений
                logging.info(f"Получено сообщение: {msg.value.decode()}")
                yield msg  # Возвращаем сообщение, позволяя продолжить чтение
        except Exception as ex:
            logging.error(f"Ошибка в цикле потребления: {ex}")
        finally:
            await self.consumer.stop()

