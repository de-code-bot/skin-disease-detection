import tomllib
from typing import Annotated, Any, Final, Optional, Self
from pathlib import Path

from backend.config.processing import check_port_availability, process_app_root, process_image_mimetypes

import pydantic

__all__ = ('QuartConfig', 'make_config')

class QuartConfig(pydantic.BaseModel):
    '''Configuration Object for Quart application'''
    APPLICATION_ROOT: Annotated[str, pydantic.Field(frozen=True, min_length=1), pydantic.BeforeValidator(process_app_root)]
    
    HOST: Annotated[pydantic.IPvAnyAddress, pydantic.Field(frozen=True)]
    PORT: Annotated[int, pydantic.Field(frozen=True, ge=0, le=64738)]

    ACCEPTED_IMAGE_MIMETYPE: Annotated[str, pydantic.BeforeValidator(process_image_mimetypes)]

    @pydantic.model_validator(mode='after')
    def validate_port(self) -> Self:
        if not check_port_availability(self.PORT):
            raise ValueError(f'Port {self.PORT} is currently running a TCP process, and cannot be used by server as listening port')
        return self
    
def make_config(config_path: Optional[Path] = None) -> QuartConfig:
    if not config_path:
        config_path = Path(__file__).parent / 'app_config.toml'
    
    with open(config_path, mode='rb') as config_file:
        return QuartConfig.model_validate(tomllib.load(config_file), strict=True)