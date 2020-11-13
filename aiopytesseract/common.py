"""
Author
------
- Yuval Kaneti.

Purpose 
--------
- Constants & Common Variables For aiopytesseract.
"""

## Imports
import asyncio
import logging

STDIN = 'stdin'
STDOUT = 'stdout'
DEFAULT_CONFIG = ''
DEFAULT_LANGUAGE = 'eng'
DEFAULT_TESSERACT_SINGLE_THREADED = True
MAX_WORKERS = 50
DEFAULT_SEMAPHORE = asyncio.Semaphore(MAX_WORKERS)

BUFFER_SIZE = 4028
READ_BYTES = 'rb'

DEBUG = True
LOGGING_FORMAT_DEBUG = "%(levelname)s - %(name)s - [%(filename)s:%(lineno)s] - %(asctime)s >> %(message)s"
LOGGING_FORMAT_PROD = "%(levelname)s - [%(filename)s:%(lineno)s] - %(asctime)s >> %(message)s"
LOGGING_FORMAT = LOGGING_FORMAT_DEBUG if DEBUG else LOGGING_FORMAT_PROD
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO



DEPRECATION_WARNING = "Function <{}> is Deprecated & will be Removed in Future Versions."
DEPRECATION_WARNING_EXCHANGE = DEPRECATION_WARNING +" Use {} Instead." 
STACKLEVEL = 1