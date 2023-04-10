from fastapi import Security
from fastapi.security.api_key import APIKeyHeader, HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from functools import wraps
import os


api_key_header = APIKeyHeader(name='access_token', auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.environ.get('APIKEY'):
        return HTTP_200_OK
    else:
        return HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Не сходиться API KEY')
    
