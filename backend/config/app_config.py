'''Configuration objects used by the Quart backend'''

from typing import Annotated, Self

from backend.config.processing import check_port_availability, process_app_root, process_http_claim

import pydantic

__all__ = ('QuartConfig',
           'ServerConfig')

class QuartConfig(pydantic.BaseModel):
    '''Configuration Object for Quart application'''
    APPLICATION_ROOT: Annotated[str, pydantic.Field(frozen=True, min_length=1), pydantic.BeforeValidator(process_app_root)]
    
    HOST: Annotated[pydantic.IPvAnyAddress, pydantic.Field(frozen=True)]
    PORT: Annotated[int, pydantic.Field(frozen=True, ge=0, le=64738)]

    @pydantic.model_validator(mode='after')
    def validate_port(self) -> Self:
        if not check_port_availability(self.PORT):
            raise ValueError(f'Port {self.PORT} is currently running a TCP process, and cannot be used by server as listening port')
        return self
    
class ServerConfig(pydantic.BaseModel):
    '''Configuration object for constants'''
    form_mimetype: Annotated[str, pydantic.Field(frozen=True, default='multipart'), pydantic.BeforeValidator(process_http_claim)]
    form_subtype: Annotated[str, pydantic.Field(frozen=True, default='form-data'), pydantic.BeforeValidator(process_http_claim)]

    max_image_size: Annotated[int, pydantic.Field(ge=1)]
    new_data_lookback_threshold: Annotated[int, pydantic.Field(ge=1)]