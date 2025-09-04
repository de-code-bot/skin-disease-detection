'''Script for creating disease_classifications table'''
import sqlite3
from typing import Final
import sys
import os

__all__ = ('main',)

def main(database_path: str) -> None:
    with sqlite3.connect(database_path) as conn:
        cursor: Final[sqlite3.Cursor] = conn.cursor()
        with open(os.path.join(os.path.dirname(__file__), 'genesis.sql'), 'r') as genesis_script:
            cursor.executescript(genesis_script.read())
        
        conn.commit()

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv[1])
