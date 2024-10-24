import requests

from app.CollectData.Params import Params


class DataCollector:
    __url = "https://api.hh.ru/vacancies"

    def __init__(self, professional_role=96, page=0, per_page=20):
        self.__params = Params(professional_role, page, per_page)

    def set_params(self, professional_role, page, per_page):
        self.__params.professional_role = professional_role
        self.__params.page = page
        self.__params.per_page = per_page

    def get_deteals_vacancies(self, vacancy_id):
        vacancy_details_response = requests.get(self.__url + f"/{vacancy_id}")
        if vacancy_details_response.status_code == 200:
            vacancy_details = vacancy_details_response.json()
            print(f"got vacancy_detaild with id: {vacancy_id}")
            return vacancy_details
        else:
            print(f"Не удалось получить детали вакансии: {vacancy_details_response.status_code}")
            return None

    def get_it_vacancies(self):
        params = self.__params.get_params()
        # Выполняем GET запрос
        response = requests.get(self.__url, params=params)

        # Проверяем статус ответа
        if response.status_code == 200:
            # Возвращаем данные в формате JSON
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
