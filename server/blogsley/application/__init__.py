from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from tortoise import Tortoise

from ariadne.asgi import GraphQL

from blogsley.schema import create_schema
from blogsley.resolver import *

app = None

async def on_startup():
    pass

async def on_shutdown():
    await Tortoise.close_connections()

def create_app(debug=True):
    global app
    if app:
        return app

    app = Starlette(
        debug=debug,
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
    app.mount("/graphql", GraphQL(schema, debug=debug))
    return app