import json
import logging

from aiokafka import AIOKafkaProducer

logging.basicConfig(level=logging.INFO)


class ProducerKafka:
    __producer_conf = {
        'bootstrap.servers': 'kafka:9092',
    }

    def __init__(self):
        pass

    async def deliver_message(self, message: str, topic):
        producer = AIOKafkaProducer(
            bootstrap_servers='kafka:9092'
        )
        # Ожидаем подключения продюсера
        await producer.start()
        try:
            # Отправляем сообщение в Kafka
            data = json.dumps(message)
            await producer.send_and_wait(topic, data.encode('utf-8'))
            logging.info(f"Сообщение отправлено в Kafka на тему {topic}: {data}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения в Kafka: {e}")
        finally:
            # Останавливаем продюсера
            await producer.stop()
