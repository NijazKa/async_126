import asyncpg
import logging

logging.basicConfig(level=logging.INFO)

async def create_connection():
    return await asyncpg.connect(
        user="postgres",
        password="7777777",
        database="async_db",
        host="localhost"
    )

async def insert_character(conn, character_data):
    query = """
    INSERT INTO characters (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    """
    await conn.execute(query, *character_data)

async def insert_all_characters(characters):
    conn = await create_connection()
    async with conn.transaction():
        for character in characters:
            properties = character["result"]["properties"]
            character_data = (
                int(character["result"]["uid"]),  # Используем `uid` вместо `id`
                properties["birth_year"],
                properties["eye_color"],
                properties["gender"],
                properties["hair_color"],
                properties["homeworld"],
                properties["mass"],
                properties["name"],
                properties["skin_color"]
            )
            await insert_character(conn, character_data)
    await conn.close()

