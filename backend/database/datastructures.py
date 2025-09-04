'''Utility data structures for database I/O'''

import os
from datetime import datetime
from typing import Iterator, TypeAlias, IO

__all__ = ('DatabaseEntry',
           'DatabaseEntryQueue')

DatabaseEntry: TypeAlias = tuple[str,str,str,str,datetime]

class DatabaseEntryQueue:
    __slots__ = ('_entry_buffer',)

    _entry_buffer: list[DatabaseEntry]

    def __init__(self) -> None:
        self._entry_buffer = []

    def __len__(self) -> int:
        return len(self._entry_buffer)
    
    def __iter__(self) -> Iterator[DatabaseEntry]:
        return iter(self._entry_buffer)
    
    def __getitem__(self, index: int) -> DatabaseEntry:
        if (0 > index or len(self) < index):
            raise IndexError
        return self._entry_buffer[index]
    
    def slice_batch(self, batch_size: int) -> list[DatabaseEntry]:
        return self._entry_buffer[:batch_size]
    
    def push_entry(self,
                   image_name: str,
                   extension: str,
                   image_path: str | os.PathLike[str] | IO[bytes],
                   classification: str,
                   processed_at: datetime
                   ) -> None:
        self._entry_buffer.append((image_name, extension, str(image_path), classification, processed_at))

    def trim_batch(self, batch_size: int) -> None:
        self._entry_buffer = self._entry_buffer[batch_size:]
