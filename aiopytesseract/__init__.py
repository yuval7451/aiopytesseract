"""
Author
------
- Yuval Kaneti

Purpose
-------
- An Asynchronouse & Non-Blcoking Version of pytesseract.

Usage
-----
```
    text = await aiopytesseract.image_to_string(image=image, tesseract_path=tesseract_path)
    print(text)
```
"""

__version__ = "1.0.0"
__all__ = ["image_to_string", "image_to_string_from_path"]
__doc__ = "An Asynchronouse & Non-Blcoking Version of pytesseract."

from .utils import LoggingFactory
from .common import LOGGING_LEVEL
Logger = LoggingFactory(__name__, LOGGING_LEVEL)

from .tesseract import image_to_string, image_to_string_from_path
from .decorators import async_performance, sync_performance