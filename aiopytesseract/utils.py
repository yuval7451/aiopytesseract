"""
Author
------
- Yuval Kaneti

Purpose
-------
- Utility Functions For aiopytesseract.
"""

## Imports
import logging
import aiofiles

from .common import  LOGGING_FORMAT, LOGGING_LEVEL, READ_BYTES, BUFFER_SIZE

## Functions
def LoggingFactory(name: str, level: int=LOGGING_LEVEL) -> logging.Logger:
    """LoggingFactory: A Logging util for FastIO.
    Parameters
    ----------
    name : str
        The Logger name.

    level : int, optional
        The Logging Level, by default LOGGING_LEVEL.
        
    Returns
    -------
    logging.Logger
        The Logger.
    """    
    Logger = logging.getLogger(name)
    Logger.setLevel(level)
    StreamHandler = logging.StreamHandler()
    StreamHandler.setLevel(level)
    formatter = logging.Formatter(LOGGING_FORMAT)
    StreamHandler.setFormatter(formatter)
    Logger.addHandler(StreamHandler)
    return Logger

async def async_read(file_path: str) -> bytes:
    """async_read: Reads File Contents Asynchronousely.

    Parameters
    ----------
    file_path : str
        the File Path on disk.

    Returns
    -------
    bytes
        The file Content.
    """    
    buffer = bytes()
    async with aiofiles.open(file_path, mode=READ_BYTES) as fd: # type: ignore
        while chunk := await fd.read(BUFFER_SIZE): # type: ignore
            buffer += chunk

    return buffer
