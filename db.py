import asyncpg

async def create_connection():
    return await asyncpg.connect(
        user="postgres",
        password="7777777",
        database="async_db",
        host="localhost"
    )

async def insert_character(conn, character_data):
    query = """
    INSERT INTO characters (id, birth_year, eye_color, gender, hair_color, homeworld, mass, name, skin_color, films, species, starships, vehicles)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
    """
    await conn.execute(query, *character_data)

async def insert_all_characters(characters): # добавил недостающие колонки
    conn = await create_connection()
    async with conn.transaction():
        for character in characters:
            character_data = (
                character["id"],
                character["birth_year"],
                character["eye_color"],
                character["gender"],
                character["hair_color"],
                character["homeworld"],
                character["mass"],
                character["name"],
                character["skin_color"],
                character["films"],
                character["species"],
                character["starships"],
                character["vehicles"]
            )
            await insert_character(conn, character_data)
    await conn.close()

