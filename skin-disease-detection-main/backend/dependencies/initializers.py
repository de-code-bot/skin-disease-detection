from pathlib import Path
from typing import Any, Final

from backend.config.app_config import ServerConfig, QuartConfig
from backend.config.processing import make_config

import keras

__all__ = ('init_server_config',
           'init_app_config',
           'init_image_classifier')

def init_server_config(config_filepath: Path) -> ServerConfig:
    return ServerConfig.model_validate(make_config(model=ServerConfig, config_path=config_filepath))

def init_app_config(config_filepath: Path) -> QuartConfig:
    return QuartConfig.model_validate(make_config(model=QuartConfig, config_path=config_filepath))

def init_image_classifier(h5_filepath: Path) -> keras.Model:
    deserialized_obj: Final[Any] = keras.models.load_model(h5_filepath)
    if not isinstance(deserialized_obj, keras.Model):
        raise RuntimeError(f'Deserialized h5 file does not return object of type {keras.Model}')
    
    return deserialized_obj