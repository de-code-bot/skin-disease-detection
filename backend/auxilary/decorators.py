from functools import wraps
from quart import request, g
from werkzeug.exceptions import BadRequest
from typing import Callable

def enforce_mimetype(type_: str, subtype: str):
    def outer_decorator(endpoint: Callable):
        @wraps(endpoint)
        def inner_decorator(*args, **kwargs):
            request_type, request_subtype = request.mimetype.split('/')
            if request_type != type_ or (request_subtype != '*' and request_subtype != subtype):
                raise BadRequest(f"Request media type must have type {type_}, with subtype {subtype}, got {request.mimetype} instead")
            return endpoint(*args, **kwargs)
        return inner_decorator
    return outer_decorator