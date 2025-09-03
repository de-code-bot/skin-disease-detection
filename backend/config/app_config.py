'''Configuration objects used by the Quart backend'''

import json
from pathlib import Path
from typing import Annotated, Self

from backend.config.processing import check_port_availability, process_app_root

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
    max_image_size: Annotated[int, pydantic.Field(ge=1)]
    image_download_buffer_size: Annotated[int, pydantic.Field(ge=1)]
    image_bucket: Annotated[Path, pydantic.BeforeValidator(lambda i : Path(i))]

    new_data_lookback_threshold: Annotated[int, pydantic.Field(ge=1)]
    classifier_h5_filename: Annotated[str, pydantic.Field(frozen=True)]
    classifier_types: dict[int, str] = {}

    def prepend_bucket_path(self, parent_dir: Path) -> Path:
        self.image_bucket = parent_dir / self.image_bucket
        if not (self.image_bucket.is_dir()):
            raise ValueError(f'Path to image bucket ({str(self.image_bucket)}) is not a directory')
        if not (self.image_bucket.is_absolute()):
            raise ValueError(f'Directory path to image bucket must be absolute')
        return self.image_bucket
    
    def populate_classifier_types(self, mapping_filepath: Path) -> dict[int, str]:
        if self.classifier_types:
            raise ValueError(f'Classifier types already populated: {self.classifier_types}')
        
        if not (mapping_filepath.is_absolute() and mapping_filepath.is_file()):
            raise ValueError(f'Path to disease categories must be an absolute filepath, got: {mapping_filepath}')
        
        self.classifier_types = {int(k) : v for k,v in json.loads(mapping_filepath.read_text(encoding='utf-8')).items()}
        return self.classifier_types
