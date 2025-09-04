'''Script for populating disease_classifications table'''
import argparse
import json
import sqlite3
import tomllib
from pathlib import Path
from typing import Any, Optional

__all__ = ('main',)

def main(categories_path: Optional[str] = None, database_path: Optional[str] = None) -> None:
    base_dir: Path = Path(__file__).parent.parent  # Traverse upwards to ./../backend, based on the assumption that an instance directory is at the same level as this package
    
    if not categories_path:
        categories_path = str(base_dir / 'classification' / 'categories.json')
    
    categories: dict[int, str] = {}
    with open(categories_path, 'r', encoding='utf-8') as categories_file:
        categories = json.loads(categories_file.read())
    
    if not database_path:
        config_dict: dict[str, dict[str, Any]] = tomllib.loads((base_dir / 'config' / 'server_config.toml').read_text(encoding='utf-8'))
        database_path = str(base_dir / 'instance' / config_dict.get('database', {}).get('database_path', 'test.db'))

    with sqlite3.connect(database_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executemany('''INSERT INTO disease_classifications
                        VALUES (?, ?)''',
                        tuple(categories.items()))
        conn.commit()


argument_parser: argparse.ArgumentParser = argparse.ArgumentParser('db_populator')
argument_parser.add_argument('--categories-path')
argument_parser.add_argument('--database-path')

if __name__ == '__main__':
    parsed_args: argparse.Namespace = argument_parser.parse_args()
    main(**parsed_args.__dict__)

