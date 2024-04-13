import logging

from fastapi.security import OAuth2PasswordBearer
from firebase_admin.exceptions import InvalidArgumentError
from fastapi import Depends
from baski.concurrent import as_async
from http import HTTPStatus
from typing import Annotated
from fastapi import HTTPException, Request
from firebase_admin import initialize_app, auth


__all__ = ['get_user']


firebase_app=initialize_app()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


async def get_user(authorization: Annotated[str | None, Header()], request: Request):
    print(request.headers)
    if not authorization:
        raise HTTPException(HTTPStatus.FORBIDDEN.value, HTTPStatus.FORBIDDEN.phrase)
    try:
        decoded_token = await as_async(auth.verify_id_token, token, firebase_app)
        user = await as_async(auth.get_user,decoded_token['uid'], firebase_app)
        return user
    except (ValueError, InvalidArgumentError) as e:
        logging.error(f'Exception while process authorization header: {e}')
        raise HTTPException(HTTPStatus.FORBIDDEN.value, HTTPStatus.FORBIDDEN.phrase)
