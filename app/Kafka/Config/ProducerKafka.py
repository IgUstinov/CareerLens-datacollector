import json

from confluent_kafka import Producer


class ProducerKafka:
    __producer_conf = {
        'bootstrap.servers': 'kafka:9092',
    }

    def __init__(self):
        pass

    def deliver_message(self, message:dict, topic):
        try:
            producer=self.get_producer()
            producer.produce(topic, json.dumps(message), callback=self.delivery_report)
            producer.flush()
        except KeyboardInterrupt:
            pass

    def delivery_report(self, err, msg):
        """Функция обратного вызова, вызываемая при доставке сообщения."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def get_producer(self):
        producer = Producer(self.__producer_conf)
        return producer
