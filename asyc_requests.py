import aiohttp
import asyncio


async def fetch_data(session, url):
    while True:
        try:
            async with session.get(url) as response:
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    print(f"Слишком много запросов. Повтор через {retry_after}")
                    await asyncio.sleep(retry_after)
                    continue
                return await response.json()
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")
            await asyncio.sleep(5)

async def fetch_planet_name(session, url):
    planet_data = await fetch_data(session, url)
    return planet_data["result"]["properties"]["name"]

async def fetch_character(session, semaphore, character_id):
    async with semaphore:
        url = f"https://www.swapi.tech/api/people/{character_id}"
        character = await fetch_data(session, url)
        properties = character["result"]["properties"]

        homeworld_url = properties["homeworld"] # получаем название планеты
        homeworld_name = await fetch_planet_name(session, homeworld_url)

        films = ",".join([film.split("/")[-2] for film in properties.get("films", [])])  # преобразуем списки в строки
        species = ",".join([specie.split("/")[-2] for specie in properties.get("species", [])])
        starships = ",".join([starship.split("/")[-2] for starship in properties.get("starships", [])])
        vehicles = ",".join([vehicle.split("/")[-2] for vehicle in properties.get("vehicles", [])])

        return {
            "id": int(character["result"]["uid"]),
            "birth_year": properties["birth_year"],
            "eye_color": properties["eye_color"],
            "gender": properties["gender"],
            "hair_color": properties["hair_color"],
            "homeworld": homeworld_name,
            "mass": properties["mass"],
            "name": properties["name"],
            "skin_color": properties["skin_color"],
            "films": films,
            "species": species,
            "starships": starships,
            "vehicles": vehicles
        }

async def fetch_all_characters():
    semaphore = asyncio.Semaphore(10)  # по задаче ограничиваем количество одновременных запросов
    async with aiohttp.ClientSession() as session:
        tasks = []
        character_id = 1
        while True:
            try:
                task = asyncio.create_task(fetch_character(session, semaphore, character_id))
                tasks.append(task)
                character_id += 1
            except Exception as e:
                print(f"Ошибка при создании персонажа {character_id}: {e}")
                break
        return await asyncio.gather(*tasks)
