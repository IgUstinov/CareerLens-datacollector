import asyncio
from fastapi import FastAPI
from app.WorkWithSignals import WorkWithSignals
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def lifespan(app: FastAPI):
    logging.info("Инициализация первых компонентов")

    wws = WorkWithSignals(base_url="https://api.hh.ru")
    loop = asyncio.get_event_loop()

    task = loop.create_task(wws.start())

    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)


# Простой эндпоинт для проверки работы сервиса
@app.get("/")
async def root():
    return {"message": "FastAPI сервис работает!"}
