from blinker import signal

from app.CollectData.DataCollector import DataCollector
from app.Kafka.KafkaProvider import KafkaProvider
from app.Provider.DbProvider import DbProvider


class WorkWithSignals:
    __dbProvider = DbProvider()


    def __init__(self,professional_role=96, page=0, per_page=20):

        self.__signals={"SignalFromBackend": signal('start_collect_data'), "SignalFromUs": signal('send_data_to_kafka')}
        self.__collector = DataCollector(professional_role, page, per_page)
        self.__kafkaProvider = KafkaProvider(self.__signals)
        self.__kafkaProvider.start_collecting_data("Backend")

    def setSignals(self):
        self.__signals["SignalFromBackend"].connect(self.got_message_from_backend)
        self.__signals["SignalFromUs"].connect(self.added_data_to_mongodb)
        return self
    def got_message_from_backend(self,msg):
        if msg['collectData'] is not None:
            data = self.__collector.get_it_vacancies()
            result = self.__dbProvider.get_NoFilerRepo().post_data(data)
            self.__signals["SignalFromUs"].send(result)
        if msg['filterData'] is not None:
            pass
    #     todo: add choice with filterData

    def added_data_to_mongodb(self,ids):
        self.__kafkaProvider.produce_kafka(ids,"python")

