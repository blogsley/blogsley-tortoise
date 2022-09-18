import jwt
import datetime

from loguru import logger

from blogsley.config import config


def encode_auth_token(**kwargs):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=0),
        'iat': datetime.datetime.utcnow()
    }

    for key, value in kwargs.items():
        payload[key] = value

    return jwt.encode(
        payload=payload,
        key=config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def decode_auth_token(request):
    logger.debug(request.headers)
    auth_token = request.headers.get('Authorization')
    logger.debug(auth_token)
    secret = config.get('SECRET_KEY')
    logger.debug(secret)
    if not auth_token:
        auth_token = ''
    try:
        payload = jwt.decode(
            jwt=auth_token,
            key=config.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
