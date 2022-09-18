from loguru import logger

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from blogsley.schema import query, mutation, subscription
from .schema import ImageConnection, ImageEdge, ImageNode
from .hub import hub, ImageSubscriber, ImageEvent
from .entity import Image

# Initialise model structure early. This does not init any database structures
Tortoise.init_models(["blogsley.models"], "models")

ImageDto = pydantic_model_creator(Image)
ImageDtoList = pydantic_queryset_creator(Image)

# Queries

@query.field("Image")
async def resolve_Image(*_, id):
    #return Image[id]
    return await Image.get(id=id)

@query.field("allImages")
async def resolve_all_Images(_, info, after:str=None, before:str=None, first:int=0, last:int=0):
    Images = await ImageDtoList.from_queryset(Image.all())
    connection = ImageConnection(Images.__root__)
    result = connection.wire()
    #print(result)
    return result

# Mutations

@mutation.field("updateImage")
async def resolve_update_Image(_, info, id, data):
    logger.debug('Image:update')
    #print(data)
    Image = await Image[id]
    Image.update_from_dict(data)
    await Image.save()
    event = ImageEvent(id, 'update')
    await hub.send(event)
    return event

# Subscriptions

@subscription.source("ImageEvents")
async def events_generator(obj, info, id=None):
    logger.debug('events_generator:begin')
    subscriber = ImageSubscriber(id)
    hub.subscribe(subscriber)
    while subscriber.active:
        event = await subscriber.receive()
        logger.debug('events_resolver:while')
        logger.debug(event)
        yield event

@subscription.field("ImageEvents")
def events_resolver(event, info, id=None):
    logger.debug('events_resolver')
    logger.debug(event)
    return event