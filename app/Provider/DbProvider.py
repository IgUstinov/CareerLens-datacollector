from app.MongoDB.FilterRepository import FilterRepository
from app.MongoDB.NoFilterRepository import NoFilterRepository

class DbProvider:
    __noFilterRepo: NoFilterRepository = NoFilterRepository()
    __filterRepo: FilterRepository = FilterRepository()

    def get_NoFilerRepo(self):
        return self.__noFilterRepo

    def get_FilterRepo(self):
        return self.__filterRepo
