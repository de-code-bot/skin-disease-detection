from functools import wraps
from quart import request, g
from werkzeug.exceptions import BadRequest
from typing import Callable

def enforce_mimetype(mimetype: str):
    def outer_decorator(endpoint: Callable):
        @wraps(endpoint)
        def inner_decorator(*args, **kwargs):
            if request.mimetype != mimetype:
                raise BadRequest(f"Request mimetype must be {mimetype}, got {request.mimetype} instead")
            return endpoint(*args, **kwargs)
        return inner_decorator
    return outer_decorator