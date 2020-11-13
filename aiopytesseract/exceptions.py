"""
Author
------
- Yuval Kaneti

Purpose
-------
- Exception Handlers For aiopytesseract.
"""

class TesseractNotFoundError(EnvironmentError):
    def __init__(self, tesseract_path):
        super(TesseractNotFoundError, self).__init__(
            f"{tesseract_path} is not installed or it's not in your PATH. \
            See README file for more information.",
        )

