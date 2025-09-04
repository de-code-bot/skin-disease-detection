'''Background tasks to be scheduled at runtime'''

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Final

import aiosqlite

from backend.dependencies.initializers import init_image_classifier
from backend.database.datastructures import DatabaseEntry, DatabaseEntryQueue

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

async def database_batch_writer(database_filepath: Path,
                                entries_queue: DatabaseEntryQueue,
                                write_lock: asyncio.Lock,
                                flush_interval: float,
                                batch_size: int,
                                lock_contention_timeout: float) -> None:
    if not (database_filepath.absolute() and database_filepath.is_file() and database_filepath.suffix == '.db'):
        raise ValueError(f'Database writer requires an absolute SQLite filepath to be provided')
    
    async with aiosqlite.connect(database_filepath) as connection:
        while True:
            try:
                await asyncio.wait_for(write_lock.acquire(), lock_contention_timeout)
                if entries_queue:
                    entry_buffer: list[DatabaseEntry] = entries_queue.slice_batch(batch_size)
                    print(entry_buffer, type(entry_buffer), flush=True)
                    await connection.executemany('''INSERT INTO image_logs (image_name, extension, image_path, classification, processed_at)
                                                VALUES (?,?,?,?,?)''',
                                                entry_buffer)

                    await connection.commit()
                    entries_queue.trim_batch(batch_size)
                write_lock.release()
            except asyncio.TimeoutError:
                ... # Maybe add some logging?
            finally:
                if write_lock.locked():
                    write_lock.release()

            await asyncio.sleep(flush_interval)