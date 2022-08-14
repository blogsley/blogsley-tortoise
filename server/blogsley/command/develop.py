import asyncio

import uvicorn

from blogsley.db import init_db

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

async def _develop():
    await init_db()

    config = uvicorn.Config(
        'blogsley.application:create_app',
        host="0.0.0.0",
        port=4000,
        reload=True,
        #reload_excludes=["build"],
        #reload_includes=["content"],
        log_level="info",
        factory=True
    )

    server = uvicorn.Server(config)
    await server.serve()

def develop():
    asyncio.run(_develop())

if __name__ == "__main__":
    develop()
