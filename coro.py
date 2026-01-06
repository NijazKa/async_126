import asyncio
from asyc_requests import fetch_all_characters
from db import insert_all_characters

async def main():
    try:
        print("Начало выгрузки данных")
        characters = await fetch_all_characters()
        print("Начало загрузки в базу")
        await insert_all_characters(characters)
        print('Выгрузка завершена')

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
