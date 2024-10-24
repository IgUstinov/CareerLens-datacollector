from app.MongoDB.NoFilterRepository import NoFilterRepository


class DbProvider:
    __noFilterRepo: NoFilterRepository = NoFilterRepository()


    def get_NoFilerRepo(self):
        return  self.__noFilterRepo