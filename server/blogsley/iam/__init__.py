from loguru import logger

from blogsley.auth.jwt import decode_auth_token
from blogsley.user import User

async def iam(info):
    logger.debug(info.context)
    token = decode_auth_token(info.context['request'])
    logger.debug(token)
    id = token['id']
    return await User.get(id=id)
