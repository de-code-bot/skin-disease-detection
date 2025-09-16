'''Script for creating disease_classifications table'''
import argparse
import sqlite3
import tomllib
from pathlib import Path
from typing import Any, Optional

__all__ = ('main',)

def main(database_path: Optional[str] = None) -> None:
    if not database_path:
        base_dir: Path = Path(__file__).parent.parent  # Traverse upwards to ./../backend, based on the assumption that an instance directory is at the same level as this package
        config_dict: dict[str, dict[str, Any]] = tomllib.loads((base_dir / 'config' / 'server_config.toml').read_text(encoding='utf-8'))
        database_path = str(base_dir / 'instance' / config_dict.get('database', {}).get('database_path', 'test.db'))
    
    if not Path(database_path).exists():
    Path(database_path).parent.mkdir(parents=True)
    
    with sqlite3.connect(database_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        sql_script: str = (Path(__file__).parent / 'genesis.sql').read_text(encoding='utf-8')
        cursor.executescript(sql_script)
        conn.commit()

argument_parser: argparse.ArgumentParser = argparse.ArgumentParser('db_genesis')
argument_parser.add_argument('--database-path')

if __name__ == '__main__':
    parsed_args: argparse.Namespace = argument_parser.parse_args()
    main(**parsed_args.__dict__)