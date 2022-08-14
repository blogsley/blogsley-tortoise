from loguru import logger

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from blogsley.schema import query, mutation, subscription
from blogsley.post.schema import PostConnection, PostEdge, PostNode
from blogsley.post.hub import hub, PostSubscriber, PostEvent
from blogsley.post.entity import Post

# Initialise model structure early. This does not init any database structures
Tortoise.init_models(["blogsley.models"], "models")

PostDto = pydantic_model_creator(Post)
PostDtoList = pydantic_queryset_creator(Post)

# Queries

@query.field("post")
async def resolve_post(*_, id):
  #return Post[id]
  return await Post.get(id=id)

@query.field("allPosts")
async def resolve_all_posts(_, info, after:str=None, before:str=None, first:int=0, last:int=0):
    posts = await PostDtoList.from_queryset(Post.all())
    connection = PostConnection(posts.__root__)
    result = connection.wire()
    #print(result)
    return result

# Mutations

@mutation.field("updatePost")
async def resolve_update_post(_, info, id, data):
    logger.debug('post:update')
    #print(data)
    request = info.context["request"]
    Post[id].set(**data)
    event = PostEvent(id, 'update')
    await hub.send(event)

# Subscriptions

@subscription.source("postEvents")
async def events_generator(obj, info, id=None):
    logger.debug('events_generator:begin')
    subscriber = PostSubscriber(id)
    hub.subscribe(subscriber)
    while subscriber.active:
        event = await subscriber.receive()
        logger.debug('events_resolver:while')
        logger.debug(event)
        yield event

@subscription.field("postEvents")
def events_resolver(event, info, id=None):
    logger.debug('events_resolver')
    logger.debug(event)
    return event