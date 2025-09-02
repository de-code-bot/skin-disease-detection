from quart import jsonify
import traceback

def generic_error_handler(e : Exception):
    '''Return a JSON formatted error message to the client
    
    Contents of the error message are determined by the following:
    - e.message: Error message
    - e.kwargs: Additonal information about the error, attached to HTTP body
    - e.header_kwargs: Additional information (e.g. server's state, broader context of the error message), attached in HTTP headers

    All of these attributes are dictionaries and are **optional**, since in their absense a generic HTTP 500 code is thrown
    '''
    print(traceback.format_exc())
    response = jsonify({"message" : getattr(e, "description", "An error occured"),
                        **getattr(e, "kwargs", {})})
    if (header_kwargs:=getattr(e, "header_kwargs", None)):
        response.headers.update(header_kwargs)

    return response, getattr(e, "code", 500)