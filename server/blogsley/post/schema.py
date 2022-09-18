from pydantic import BaseModel

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from blogsley.schema import query, mutation, subscription
from blogsley.schema.schemata import Connection, Edge, Node

from .entity import Post

# Initialise model structure early. This does not init any database structures
Tortoise.init_models(["blogsley.models"], "models")

PostDto = pydantic_model_creator(Post)
PostDtoList = pydantic_queryset_creator(Post)

class PostInput(BaseModel):
    title: str
    block: str
    body: str

class PostNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class PostEdge(Edge):
    def __init__(self, obj, node_class=PostNode):
        super().__init__(obj, node_class)

class PostConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PostEdge, node_class=PostNode)
