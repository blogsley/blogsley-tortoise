from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from tortoise import Tortoise

from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler

from blogsley.schema import create_schema
from blogsley.resolver import *
from blogsley.db import init_db

DEBUG = True
app = None

async def on_startup():
    await init_db()

async def on_shutdown():
    await Tortoise.close_connections()

def create_app():
    global app
    if app:
        return app

    app = Starlette(
        debug=DEBUG,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    schema = create_schema()
    app.mount("/graphql", GraphQL(
        schema,
        debug=DEBUG,
        #websocket_handler=GraphQLTransportWSHandler(),
    ))
    return app