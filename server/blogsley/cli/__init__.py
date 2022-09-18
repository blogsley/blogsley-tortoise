import os
import click

from .group import BlogsleyGroup, BlogsleyInfo
from .serve import serve
from .develop import dev
from .populate import populate


@click.group(cls=BlogsleyGroup)
@click.pass_context
def entry_point(ctx):
    ctx.ensure_object(BlogsleyInfo)

entry_point.add_command(serve)
entry_point.add_command(dev)
entry_point.add_command(populate)
