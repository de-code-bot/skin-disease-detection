from functools import wraps
from typing import Any, Callable, Coroutine

from werkzeug.exceptions import BadRequest
from quart import request, Response

from backend.models.requests import RequestMimes

def enforce_mimetype(type_: RequestMimes, subtype: RequestMimes):
    def outer_decorator(endpoint: Callable[..., Coroutine[Any, Any, tuple[Response, int]]]):
        @wraps(endpoint)
        async def inner_decorator(*args, **kwargs):
            request_type, request_subtype = request.mimetype.split('/')
            if request_type != type_ or (request_subtype != '*' and request_subtype != subtype):
                raise BadRequest(f"Request media type must have type {type_}, with subtype {subtype}, got {request.mimetype} instead")
            return await endpoint(*args, **kwargs)
        return inner_decorator
    return outer_decorator