import asyncio
import os
import threading
import aiohttp
import json
import aiofiles


WEB_URI = "http://web-api:8000/api/data"
FILE_PATH = 'background/output.txt'

async def fetch_and_save_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB_URI) as response:
            data = await response.json()
            text = await format_data(data)
            await save_to_file(text)


async def format_data(data):
    text = await json.load(data)
    result = await json.dumps(text)
    return result


async def save_to_file(data):
    # Асинхронно сохраняем данные в файл
    async with aiofiles.open(FILE_PATH, mode="a") as file:
        await file.write(data)


async def periodic_task(interval_seconds):
    while True:
        await fetch_and_save_data()
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    threads = []
    for _ in range(int(os.environ['NUMBER_THREADS'])):
        thread = threading.Thread(target=periodic_task, args=[20])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
