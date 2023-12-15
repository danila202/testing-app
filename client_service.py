import asyncio
import aiohttp
import requests
import threading
import random
from time import sleep
import os

from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler

URI_API = '127.0.0.1:8000/api/data'
LOG_FILE_PATH = 'log'
NUMBER_THREADS = int(os.getenv('NUMBER_THREADS', 3))
DELAY = int(os.environ.get("CLIENT_DELAY_MS", 1000))
threads = []


logger = Logger.with_default_handlers(
        name="async_logger",
        level="INFO",
        handlers=[AsyncFileHandler(filename="logs.log")]
    )


async def generate_string():
    ip = random.choice(['127.0.0.1', '8.8.8.8'])
    uri = random.choice(['/path1', '/path2', '/path3'])
    http_method = random.choice(['GET', 'POST'])
    http_status_code = random.choice([201, 418])

    log = f'{ip} {http_method} {uri} {http_status_code}'
    await logger.info(log)

    return log


async def send_log_entry(log):
    async with aiohttp.ClientSession as session:
        payload = {'log': log}
        async with session.post(URI_API, json=payload) as response:
            response_json = await response.json()
            if response_json.status == 201:
                print('Лог сохранен')
            if response_json.status == 401:
                print('Что-то пошло не так')


async def main():
    log = await generate_string()
    await send_log_entry(log)
    await asyncio.sleep(DELAY/1000)

def start_client_service():
    asyncio.run(main())


if "__name__" == "__main__":
    for _ in range(NUMBER_THREADS):
        thread = threading.Thread(target=start_client_service)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


