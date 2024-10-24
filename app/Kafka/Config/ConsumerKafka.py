import json
import threading

from confluent_kafka import Consumer, KafkaException
from blinker import signal


class ConsumerKafka:
    __consumer_conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'python',
        'auto.offset.reset': 'earliest',
    }

    def __init__(self):
        pass

    def start(self, topic: str, signaler: signal):
        consumer = self.get_consumer()
        consumer.subscribe([topic])
        consumer_thread = threading.Thread(target=self.start_consume_messages, args=(consumer, signaler))
        consumer_thread.start()

    def get_consumer(self):
        consumer = Consumer(self.__consumer_conf)
        return consumer

    def start_consume_messages(self, consumer, signaler: signal):
        try:
            while True:
                msg = consumer.poll(timeout=1.0)  # ожидание сообщения
                if msg is None:  # если сообщений нет
                    continue
                if msg.error():  # обработка ошибок
                    raise KafkaException(msg.error())
                else:
                    # действия с полученным сообщением
                    message = json.loads(msg.value())
                    signaler.send(message)
                    print(f"Received message: {message}")
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()  # не забываем закрыть соединение
