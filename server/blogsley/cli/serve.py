import os
import click
import uvicorn

@click.command()
@click.pass_context
def serve(ctx):
    app = ctx.obj.app
    os.environ["BLOGSLEY_ENV"] = "production"
    _serve(app)

def _serve(app):
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
