import requests


def get_it_vacancies(page=0, per_page=20):
    # URL для поиска вакансий
    url = "https://api.hh.ru/vacancies"

    # Параметры запроса
    params = {
        "professional_role": 96,  # Поиск вакансий с IT
        "area": 1,  # Регион (1 - Москва)
        "page": page,  # Номер страницы
        "per_page": per_page,  # Количество вакансий на странице
    }

    # Выполняем GET запрос
    response = requests.get(url, params=params)

    # Проверяем статус ответа
    if response.status_code == 200:
        # Возвращаем данные в формате JSON
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        return None
