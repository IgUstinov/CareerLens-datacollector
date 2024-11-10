import json
import logging
import time

import aiohttp
import requests

from app.CollectData.Params import Params

logging.basicConfig(level=logging.INFO)


class DataCollector:
    def __init__(self, base_url):
        self.base_url = base_url

    def set_params(self, professional_role, page, per_page):
        self.__params.professional_role = professional_role
        self.__params.page = page
        self.__params.per_page = per_page

    def get_deteals_vacancies(self, vacancy_id):
        vacancy_details_response = requests.get(self.base_url + f"/{vacancy_id}")
        if vacancy_details_response.status_code == 200:
            vacancy_details = vacancy_details_response.json()
            logging.info(f"got vacancy_detaild with id: {vacancy_id}")
            return vacancy_details
        else:
            logging.info(f"Не удалось получить детали вакансии: {vacancy_details_response.status_code}")
            return None

    def get_it_vacancies(self):
        params = self.__params.get_params()
        # Выполняем GET запрос
        response = requests.get(self.base_url, params=params)

        # Проверяем статус ответа
        if response.status_code == 200:
            # Возвращаем данные в формате JSON
            return response.json()
        else:
            logging.info(f"Ошибка: {response.status_code}")
            return None

    async def get_vacancies_batches(self, max_records=10000, per_page=100) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                page = 0
                total_records = 0
                params = {
                    "professional_role": 96,
                    "page": 0,
                    "per_page": per_page
                }
                while total_records < max_records:
                    url = f"{self.base_url}/vacancies"
                    params['page'] = page
                    vacancies = await self.fetch(session, url, params=params)

                    if not vacancies or 'items' not in vacancies or len(vacancies['items']) == 0:
                        break

                    total_records += len(vacancies['items'])

                    yield vacancies['items']

                    if vacancies["pages"] <= params["page"] + 1:
                        logging.info("Все вакансии загружены.")
                        break
                    page += 1

                    if total_records >= max_records:
                        logging.info("Достигнуто максимальное количество записей")
                        break

                    time.sleep(1)
        except Exception as ex:
            logging.info(ex)

    async def get_vacancies(self, session, page, per_page=100):
        url = f"{self.base_url}/vacancies"
        params = {"page": page, "per_page": per_page}
        return await self.fetch(session, url, params=params)

    async def fetch(self, session, url, params=None):
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logging.info(f"Ошибка: {response.status}")
                    return None
        except Exception as ex:
            logging.error(ex)

    async def get_countries(self):
        url = 'https://api.hh.ru/areas'
        response = requests.get(url)
        if response.status_code == 200:
            areas = response.json()
            return areas
        else:
            print("Ошибка при получении данных:", response.status_code)