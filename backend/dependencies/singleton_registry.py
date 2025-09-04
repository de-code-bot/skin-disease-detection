import asyncio
from typing import Any, Callable, Annotated
from typing_extensions import Self

import inspect
import functools

from backend.config.app_config import ServerConfig
import keras

import pydantic

from backend.config.app_config import ServerConfig
from backend.dependencies.singleton_types import AppImageClassifierType, ServerConfigurationType, DatabaseEntryQueueType
from backend.database.datastructures import DatabaseEntryQueue

__all__ = ('SingletonRegistry',)

_registryy_config_mapping = pydantic.ConfigDict({
    'arbitrary_types_allowed' : True
    })

class SingletonRegistry(pydantic.BaseModel):
    '''Dataclass to store all global singletons used by the server'''
    model_config: pydantic.ConfigDict = _registryy_config_mapping

    server_config: Annotated[ServerConfig, pydantic.Field(frozen=True)]
    image_classifier: keras.models.Model

    _db_entry_queue: Annotated[DatabaseEntryQueue, pydantic.Field(frozen=True)] = pydantic.PrivateAttr(default=DatabaseEntryQueue())
    _db_entry_write_lock: Annotated[asyncio.Lock, pydantic.Field(frozen=True)] = pydantic.PrivateAttr(default=asyncio.Lock())
    
    _type_mapping: dict[type, Any] = pydantic.PrivateAttr(default={})

    @pydantic.model_validator(mode='after')
    def populate_type_mapping(self) -> Self:
        self._type_mapping = {
            ServerConfigurationType : self.server_config,
            AppImageClassifierType : self.image_classifier,
            DatabaseEntryQueueType : self._db_entry_queue
        }

        return self

    @property
    def type_mapping(self) -> dict[type, Any]:
        return self._type_mapping
    
    def inject_singletons(self,
                            func: Callable[..., Any]) -> Callable[..., Any]:
        bound_args: dict[str, Any] = {}
        for paramname, param in inspect.signature(func).parameters.items():
            if param.annotation not in self.type_mapping:
                raise TypeError(f'Parameter mismatch on calling {func} with parameter {paramname} of type {param.annotation}')
            bound_args[paramname] = self.type_mapping[param.annotation]

        return functools.partial(func, **bound_args)