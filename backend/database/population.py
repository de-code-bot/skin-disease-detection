'''Script for populating disease_classifications table'''
import sqlite3
from typing import Final
import json
import sys

__all__ = ('main',)

def main(database_path: str, categories_path: str) -> None:
    categories: dict[int, str] = {}
    with open(categories_path, 'r', encoding='utf-8') as categories_file:
        categories = json.loads(categories_file.read())
    
    with sqlite3.connect(database_path) as conn:
        cursor: Final[sqlite3.Cursor] = conn.cursor()
        cursor.executemany('''INSERT INTO disease_classifications
                           VALUES (?, ?)''',
                           tuple(categories.items()))
        conn.commit()

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv[1], sys.argv[2])
