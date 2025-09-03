'''Models related to incoming requests (post middleware)'''

from enum import StrEnum

class RequestMimes(StrEnum):
    '''Enum for expected media types from incoming HTTP requests headers'''
    WILDCARD = '*'
    
    # Types
    FORM_TYPE = 'multipart'

    # Subtypes
    FORM_SUBTYPE = 'form-data'
