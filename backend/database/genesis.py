'''Script for creating disease_classifications table'''
import os
import sqlite3
import sys
from typing import Final

__all__ = ('main',)

def main(database_path: str) -> None:
    with sqlite3.connect(database_path) as conn:
        cursor: Final[sqlite3.Cursor] = conn.cursor()
        with open(os.path.join(os.path.dirname(__file__), 'genesis.sql'), 'r') as genesis_script:
            cursor.executescript(genesis_script.read())
        
        conn.commit()

if __name__ == '__main__':
    main(sys.argv[1])
