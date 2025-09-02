'''Processing methods for config values'''

import re
import socket
import tomllib
from pathlib import Path
from typing import Any, Final

import pydantic

__all__ = ('PATH_REGEX',
           'process_app_root',
           'check_port_availability',)

PATH_REGEX: Final[re.Pattern] = re.compile(r"^/([\w\-/]*)/?$")

def process_http_claim(claim: str) -> str:
    return claim.lower().strip()

def process_app_root(root: str) -> str:
    root = root.strip().lower()
    if not PATH_REGEX.match(root):
        raise ValueError(f'Application root {root} invalid')
    return root

def check_port_availability(port: int, protocol: socket.SocketKind = socket.SOCK_STREAM) -> bool:
    '''Check whether a port is available for running a protocol.
    Args:
        port (int): Port number to check.
        protocol (socket.SocketKind): Protocol to check the port against, defaults to TCP.
        
    Returns:
        bool: Whether port is available to run the given protocol.'''
    try:
        with socket.socket(socket.AF_INET, protocol) as test_socket:
            test_socket.connect(('127.0.0.1', port))
            return False
    except (socket.timeout, ConnectionRefusedError, OSError):
        return True


def make_config(model: type[pydantic.BaseModel], config_path: Path) -> Any:
    with open(config_path, mode='rb') as config_file:
        # Config dict will need to be flattened first before being parsed by pydantic
        flattened_config_dict: dict[str, str|int] = {}
        remaining_maps: list[dict[str, Any]] = [tomllib.load(config_file)]
        
        while remaining_maps:
            map: dict[str, Any] = remaining_maps.pop()
            for k, v in map.items():
                if isinstance(v, dict):
                    remaining_maps.append(v)
                    continue
                flattened_config_dict[k] = v

        return model.model_validate(flattened_config_dict, strict=True)