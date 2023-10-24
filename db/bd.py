from os import path, getenv

from aiocache import cached
from aiocache.serializers import PickleSerializer
import aiosqlite

from config_data.config import load_config

config = load_config()
db_path: str = config.db.database_path
async def table_update(username: str, user_id: int):
    # root = path.dirname(path.realpath(__file__))
    # db = await aiosqlite.connect(path.join(root, 'fortests15.db'))
    db = await aiosqlite.connect(db_path)
    mycursor = await db.cursor()
    await mycursor.execute("""CREATE TABLE IF NOT EXISTS users_info (
            user_id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            is_admin BOOLEAN,
            blocked_until INTEGER
        )""")
    await db.commit()
    try:
        res = 1 if user_id == int(getenv('CREATOR_ID')) else 0
        await db.execute(f"INSERT INTO users_info(user_id,name,is_admin,blocked_until) VALUES (?,?,?,?)",
                         (user_id, username, res, 0))
        await db.commit()
        print("айди пользователя, айди чата и ник добавлены в бд!")
    except aiosqlite.IntegrityError as e:
        print("ошибка добавления пользователя в бд", e)
    finally:
        await mycursor.close()
        await db.close()


@cached(ttl=10, serializer=PickleSerializer())
async def DB_get_data() -> dict:
    # root = path.dirname(path.realpath(__file__))
    async with aiosqlite.connect(db_path) as connect:
        async with connect.execute("SELECT user_id,name,is_admin,blocked_until FROM users_info") as cursor:
            # users_data: list = [data for data in await cursor.fetchall()]
            user_ids, names, is_admin, bantime = zip(*(await cursor.fetchall()))
    # return [user_ids,names,is_admin]
    return {user_id: {'username': name, 'admin_key': admin, 'ban_duration': bantime} for user_id, name, admin, bantime
            in zip(user_ids, names, is_admin, bantime)}
    # return users_data


@cached(ttl=10, serializer=PickleSerializer())
async def DB_upload_data(new_status: int, parametr: str, column_name: str) -> None:
    # root = path.dirname(path.realpath(__file__))
    async with aiosqlite.connect(db_path) as connect:
        cursor = await connect.cursor()
        try:
            await cursor.execute(f"UPDATE users_info SET {column_name} = ? WHERE name = ?", (new_status, parametr))
            await connect.commit()
        except aiosqlite.Error as e:
            print(f"Ошибка при выполнении запроса:{e}")
            await connect.rollback()
        await cursor.close()
