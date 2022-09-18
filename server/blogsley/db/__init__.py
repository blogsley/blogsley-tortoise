import os

from tortoise import Tortoise

from blogsley.config import config


async def init_db():
    DB_URL = os.environ.get('DB_URL', 'sqlite://db.sqlite3')
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['blogsley.models']}
    )
    await Tortoise.generate_schemas()
