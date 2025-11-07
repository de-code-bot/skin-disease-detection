from typing import NewType

from backend.config.app_config import ServerConfig
from backend.database.datastructures import DatabaseEntryQueue

import keras

__all__ = ('ServerConfigurationType',
           'AppImageClassifierType',
           'DatabaseEntryQueueType')

AppImageClassifierType = NewType("AppImageClassifierType", keras.models.Model)
ServerConfigurationType = NewType("ServerConfigurationType", ServerConfig)
DatabaseEntryQueueType = NewType("DatabaseEntryQueueType", DatabaseEntryQueue)