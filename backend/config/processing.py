'''Processing methods for config values'''

import re
import socket
from typing import Final

__all__ = ('PATH_REGEX',
           'IMAGE_MIMETYPE_REGEX',
           'process_app_root',
           'process_image_mimetypes',
           'check_port_availability',)

PATH_REGEX: Final[re.Pattern] = re.compile(r"^/([\w\-/]*)/?$")
IMAGE_MIMETYPE_REGEX: Final[re.Pattern] = re.compile(r"^image/.*$")

def process_app_root(root: str) -> str:
    root = root.strip().lower()
    if not PATH_REGEX.match(root):
        raise ValueError(f'Application root {root} invalid')
    return root

def process_image_mimetypes(mimetype: str) -> str:
    mimetype = mimetype.strip()
    if not IMAGE_MIMETYPE_REGEX.match(mimetype):
        raise ValueError(f'Invalid mimetype for images {mimetype}')
    return mimetype

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
