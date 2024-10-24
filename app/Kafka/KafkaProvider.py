from app.Kafka.Config.ConsumerKafka import ConsumerKafka
from app.Kafka.Config.ProducerKafka import ProducerKafka
from blinker import signal


class KafkaProvider:

    def __init__(self, signals:dict):
        self.__signals = signals

    def produce_kafka(self, message, topic):
        ProducerKafka().deliver_message(message, topic)

    def start_collecting_data(self,topic: str):
        ConsumerKafka().start(topic, self.__signals["SignalFromBackend"])
