'''Methods invoked at server bootup to begin background tasks, perform logs, and initialize global singletons'''

from pathlib import Path
from typing import Any, Final

from backend.config.processing import make_config
from backend.config.app_config import QuartConfig, ServerConfig
from backend.singletons import quart_config, server_config, image_classifier

import keras

__all__ = ('init_server_config',
           'init_app_config',
           'init_image_classifier')

def init_server_config(config_filepath: Path) -> ServerConfig:
    global server_config
    server_config = make_config(model=ServerConfig, config_path=config_filepath)
    return server_config

def init_app_config(config_filepath: Path) -> QuartConfig:
    global quart_config
    quart_config = make_config(model=QuartConfig, config_path=config_filepath)
    return quart_config

def init_image_classifier(h5_filepath: Path) -> keras.Model:
    global image_classifier
    deserialized_obj: Final[Any] = keras.models.load_model(h5_filepath)
    if not isinstance(deserialized_obj, keras.Model):
        raise RuntimeError(f'Deserialized h5 file does not return object of type {keras.Model}')
    image_classifier = deserialized_obj
    return image_classifier
