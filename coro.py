import asyncio

from asyc_requests  import fetch_all_characters
from db import insert_all_characters
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        characters = await fetch_all_characters()
        await insert_all_characters(characters)
    except Exception as e:
        logging.error(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
