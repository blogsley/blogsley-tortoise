import os
import asyncio

from loguru import logger
import click
import uvicorn

import blogsley.config
from blogsley.db import init_db

@click.command()
@click.pass_context
def dev(ctx):
    logger.debug('dev')
    app = ctx.obj.app
    os.environ["BLOGSLEY_ENV"] = "debug"
    blogsley.config.debug = app.debug = True
    asyncio.run(_dev())

async def _dev():
    await init_db()

    config = uvicorn.Config(
        'blogsley.application:create_app',
        host="0.0.0.0",
        port=4000,
        debug=True,
        reload=True,
        reload_dirs=['./blogsley'],
        log_level="info",
        factory=True
    )

    server = uvicorn.Server(config)
    await server.serve()
