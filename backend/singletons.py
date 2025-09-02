from typing import Optional

from backend.config.app_config import QuartConfig, ServerConfig
import keras

__all__ = ('quart_config',
           'server_config',
           'image_classifier')

quart_config: Optional[QuartConfig] = None
server_config: Optional[ServerConfig] = None
image_classifier: Optional[keras.Model] = None