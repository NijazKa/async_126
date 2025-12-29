import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def fetch_character(session, character_id):
    url = f"https://www.swapi.tech/api/people/{character_id}"
    while True:
        try:
            async with session.get(url) as response:
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 5)) # сервер блокирует большое количество запросов, пришлось добавить задержку
                    await asyncio.sleep(retry_after)
                    continue
                return await response.json()
        except Exception as e:
            await asyncio.sleep(5)

async def fetch_all_characters():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 83):
            tasks.append(fetch_character(session, i))
            await asyncio.sleep(1)  # Задержка между запросами
        return await asyncio.gather(*tasks)
