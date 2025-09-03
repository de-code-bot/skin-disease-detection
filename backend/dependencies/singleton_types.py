from typing import NewType, TypeVar

from backend.config.app_config import ServerConfig

import keras

__all__ = ('ServerConfigurationType',
           'AppImageClassifierType')

AppImageClassifierType = NewType("AppImageClassifierType", keras.models.Model)
ServerConfigurationType = NewType("ServerConfigurationType", ServerConfig)