from loguru import logger

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from blogsley.schema import query, mutation
from blogsley.schema.schemata import Connection, Edge, Node
from blogsley.user import User
from blogsley.user.hub import hub, UserSubscriber, UserEvent

# Initialise model structure early. This does not init any database structures
Tortoise.init_models(["blogsley.models"], "models")

UserDto = pydantic_model_creator(User)
UserDtoList = pydantic_queryset_creator(User)

class UserConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=UserEdge, node_class=UserNode)


class UserEdge(Edge):
    def __init__(self, obj, node_class):
        super().__init__(obj, UserNode)


class UserNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

@query.field("user")
async def resolve_user(*_, id):
    #return User[id]
    return await User.get(id=id)

@query.field("allUsers")
async def resolve_all_users(_, info, after:str=None, before:str=None, first:int=0, last:int=0):
    users = await UserDtoList.from_queryset(User.all())
    connection = UserConnection(users.__root__)
    result = connection.wire()
    #print(result)
    return result
    
# Mutations

@mutation.field("updateUser")
async def resolve_update_user(_, info, id, data):
    logger.debug('user:update')
    #print(data)
    user = await User[id]
    user.update_from_dict(data)
    await user.save()
    event = UserEvent(id, 'update')
    await hub.send(event)
