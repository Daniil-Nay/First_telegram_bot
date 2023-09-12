from os import path

import aiosqlite

async def table_update(user_id: int, username: str):
    root = path.dirname(path.realpath(__file__))
    db = await aiosqlite.connect(path.join(root, 'users.db'))
    mycursor = await db.cursor()
    await mycursor.execute("""CREATE TABLE IF NOT EXISTS users_info (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50)
        )""")
    await db.commit()
    try:
        await db.execute(f"INSERT INTO users_info(id,name) VALUES (?,?)", (user_id, username))
        await db.commit()
        print("айди и ник добавлены в бд!")
    except aiosqlite.IntegrityError as e:
        print("ошибка добавления пользователя в бд", e)
    finally:
        await mycursor.close()
        await db.close()
