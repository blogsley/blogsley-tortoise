import os

from tortoise import Tortoise

import blogsley.config
from blogsley.config import config

#blogsley.config.db = db

async def init_db():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    DB_URL = os.environ.get('DB_URL', 'sqlite://db.sqlite3')
    await Tortoise.init(
        #db_url='sqlite://db.sqlite3',
        db_url=DB_URL,
        modules={'models': ['blogsley.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

'''
def load_db():
    db.bind(provider='postgres',
        user=os.environ.get("POSTGRES_USER", ""),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        host=os.environ.get("POSTGRES_HOST", ""),
        database=os.environ.get("POSTGRES_DB", "")
    )

    db.generate_mapping(create_tables=True)
    return db
'''