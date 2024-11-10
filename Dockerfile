# Указываем базовый образ
FROM python:3.9
EXPOSE 5678


# Устанавливаем рабочую директорию
WORKDIR /app


# Копируем зависимости
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# Копируем все файлы проекта
COPY . .


# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
