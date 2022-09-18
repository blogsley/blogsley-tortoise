from loguru import logger

from blogsley.iam import iam

from .schema import *
from .hub import hub, PostSubscriber, PostEvent
from .entity import Post

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

@mutation.field("createPost")
async def resolve_create_post(_, info, data):
    logger.debug('post:create')
    #print(data)
    post_input = PostInput(**data)
    user = await iam(info)
    post = await Post.create(author=user, **post_input.dict())
    await post.save()
    event = PostEvent(id, 'create')
    await hub.send(event)
    post_dto = PostDto.from_orm(post)
    return post_dto

@mutation.field("updatePost")
async def resolve_update_post(_, info, id, data):
    logger.debug('post:update')
    #print(data)
    post = await Post[id]
    post.update_from_dict(data)
    await post.save()
    event = PostEvent(id, 'update')
    await hub.send(event)
    return event

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