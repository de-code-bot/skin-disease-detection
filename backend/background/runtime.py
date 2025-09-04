'''Background tasks to be scheduled at runtime'''

import asyncio
from pathlib import Path

from backend.dependencies.initializers import init_image_classifier
from backend.config.app_config import ServerConfig

import keras

__all__ = ('model_swapper',)

async def model_swapper(model_filepath: Path,
                        model: keras.Model,
                        poll_interval: float,
                        extension: str = '.h5') -> None:
    if not (model_filepath.absolute() and model_filepath.is_file() and model_filepath.suffix == extension):
        raise ValueError(f'Path to model must be an absolute filepath to a file with extension {extension}. Got {model_filepath} instead')
    
    last_modified: float = model_filepath.stat().st_mtime
    while True:
        current_mtime: float = model_filepath.stat().st_mtime
        if last_modified != current_mtime:
            model = init_image_classifier(model_filepath)
            last_modified = current_mtime
        await asyncio.sleep(poll_interval)
