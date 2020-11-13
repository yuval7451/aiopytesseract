"""
Author
------
- Yuval Kaneti

Purpose
-------
- An Asynchronouse & Non-Blcoking Version of pytesseract.
"""
## Imports
import os
import shlex
import asyncio

from errno import ENOENT
from typing import Any, Dict, List

from .utils import LoggingFactory, async_read
from .decorators import async_performance, deprecated
from .exceptions import TesseractNotFoundError
from .common import DEFAULT_SEMAPHORE, DEFAULT_TESSERACT_SINGLE_THREADED, STDIN, STDOUT, DEFAULT_CONFIG, DEFAULT_LANGUAGE

Logger = LoggingFactory(__name__)



# Functions
def _get_config(config: str) -> List[str]:
    """_get_config: Return a Safe Escaped Command line config for tesseract.

    Parameters
    ----------
    config : str
        The Config passed from the user.

    Returns
    -------
    List[str]
        A List Containing the Config after being safely escaped by shelx.
    """    
    if config:
        return shlex.split(config)
    else:
        return []


def _get_language(language: str) -> List[str]:
    """_get_language: Return The language command line for tesseract.

    Parameters
    ----------
    language : str
        The language specifed by the user, all avilable languages can be found on tesseract Website.

    Returns
    -------
    List[str]
        The language command line.
    """    
    if language is not None:
        return ['-l', language]
    else:
        return []
        

def _get_subprocess_args(tesseract_path: str) -> List[str]:
    """_get_subprocess_args: Returns the base command line for tesseract.

    Parameters
    ----------
    tesseract_path : str
        The tesseract path on disk.

    Returns
    -------
    List[str]
        The base tesseract Command.
    """    
    return [tesseract_path, STDIN, STDOUT]


def _get_subprocess_kwargs(tesseract_single_threaded: bool) -> Dict[str, Any]:
    """_get_subprocess_kwargs: Returns the base sub process arguments.

    Parameters
    ----------
    tesseract_single_threaded : bool
        Sets The `OMP_THREAD_LIMIT` environment variable, 
        Should tesseract use only one thread, usefull if running many tesseract Concourantly.

    Returns
    -------
    Dict[str, Any]
        A Dict Containing asyncio.create_subprocess_exec(...) Arguments.
    """    
    if tesseract_single_threaded:
        os.environ['OMP_THREAD_LIMIT'] = '1'

    kwargs = {
        'stdin': asyncio.subprocess.PIPE,
        'stderr': asyncio.subprocess.PIPE,
        'stdout': asyncio.subprocess.PIPE,
        'startupinfo': None,
        'env': os.environ,
    }

    return kwargs


async def run_tesseract_async(image: bytes, tesseract_path: str, language: str, config: str, tesseract_single_threaded: bool) -> bytes:
    """run_tesseract_async: Run tesseract Asynchronousely and returns the output.

    Parameters
    ----------
    image : bytes
        The image data, open(ImagePath, mode='rb').read()
    
    tesseract_path : str
        The tesseract path on disk.
    
    language : str
        the language tesseract will try to extract the text in.
    
    config : str
        A Config for tesseract.
    
    tesseract_single_threaded : bool
        Should tesseract use only one thread, usefull if running many tesseract Concourantly.

    Awaits
    ------
    - asyncio.create_subprocess_exec(...) 
    - proc.communicate(...)

    Returns
    -------
    bytes
        The tesseract execution output.

    Raises
    ------
    GeneralOSError
        A Genral OS Error
    
    TesseractNotFoundError
        Tesseract Could not be Found & Executed.

    Notes
    -----
    - You Should Probably be using image_to_string or image_to_string_from_path,
      This Functions gives you more Control over the parameters for fine tunning.
    
    Usgae
    -----
    ```
        image = open(r"PATH\\TO\\IMAGE", mode="rb").read()
        text = await run_tesseract_async(image=image, tesseract_path=r"PATH\\TO\\TESSERACT", language='eng', 
                                         config='', tesseract_single_threaded=True)
        print(text)
    ```
    """    
    stdout = bytes()
    # Build Command line arguments.
    cmd_args = _get_subprocess_args(tesseract_path=tesseract_path)
    cmd_args += _get_config(config=config)
    cmd_args += _get_language(language=language)
    cmd_kwargs = _get_subprocess_kwargs(tesseract_single_threaded=tesseract_single_threaded)
    # Try Run the Tesseract Process.
    try:
        proc = await asyncio.create_subprocess_exec(*cmd_args, **cmd_kwargs)        
        stdout, _ = await proc.communicate(input=image)
    # Handle errors.
    except OSError as GeneralOSError:
        if GeneralOSError.errno != ENOENT:
            raise GeneralOSError
        raise TesseractNotFoundError(tesseract_path=tesseract_path)
    # Returns the Execution Output.
    finally:
        return stdout


@async_performance
async def image_to_string(image: bytes, tesseract_path: str, language: str=DEFAULT_LANGUAGE, 
                          config: str=DEFAULT_CONFIG, tesseract_single_threaded: bool=DEFAULT_TESSERACT_SINGLE_THREADED, semaphore: asyncio.Semaphore=None) -> bytes:
    """image_to_string: Extracts Text from a Given image Asynchronousely.

    Parameters
    ----------
    image : bytes
        The Image Data, open(ImagePath, mode='rb').read().
    
    tesseract_path : str
        The tesseract path on disk.
    
    language : str, optional
        The language tesseract will try to extract the text in, by default 'eng'
    
    config : str, optional
        A config for tesseract Runtime, by default DEFAULT_CONFIG
    
    tesseract_single_threaded : bool, optional
        Should tesseract use only one thread, usefull if running many tesseract Concourantly.
        by default True
    
    semaphore : asyncio.Semaphore, optional
        A semaphore to limit then number of concourant calls to ..run_tesseract_async(...).
        by default None

    Awaits
    ------
    -  run_tesseract_async(...)

    Returns
    -------
    bytes
        tesseract Execution output.

    Usgae
    -----
    ```
        image = open(r"PATH\\TO\\IMAGE", mode="rb").read()
        text = await image_to_string(image=image, tesseract_path=r"PATH\\TO\\TESSERACT")
        print(text)
    ```
    """ 
    async with asyncio.Semaphore() if semaphore is None else semaphore:
        return await run_tesseract_async(image=image, tesseract_path=tesseract_path, language=language, 
                                         config=config, tesseract_single_threaded=tesseract_single_threaded)


@async_performance
async def image_to_string_from_path(image_path: str, tesseract_path: str, language: str=DEFAULT_LANGUAGE, 
                          config: str=DEFAULT_CONFIG, tesseract_single_threaded: bool=DEFAULT_TESSERACT_SINGLE_THREADED, semaphore: asyncio.Semaphore=None) -> bytes:
    """image_to_string: Extracts Text from a Given image path Asynchronousely.

    Parameters
    ----------
    image_path : str
        The Path on disk to the Image.
    
    tesseract_path : str
        The tesseract path on disk.
    
    language : str, optional
        The language tesseract will try to extract the text in, by default DEFAULT_LANGUAGE
    
    config : str, optional
        A config for tesseract Runtime, by default DEFAULT_CONFIG
    
    tesseract_single_threaded : bool, optional
        Should tesseract use only one thread, usefull if running many tesseract Concourantly.
        by default DEFAULT_TESSERACT_SINGLE_THREADED
    
    semaphore : asyncio.Semaphore, optional
        A semaphore to limit then number of concourant calls to ..run_tesseract_async(...).
        by default None

    Awaits
    ------
    - run_tesseract_async(...)
    - async_read(...)

    Returns
    -------
    bytes
        tesseract Execution output.

    Notes
    -----
    - async_read(...) Opens the File Asynchronousely, This should be you first choise for more simpiler code.

    Usgae
    -----
    ```
        text = await image_to_string_from_path(image=r"PATH\\TO\\IMAGE", tesseract_path=r"PATH\\TO\\TESSERACT")
        print(text)
    ```
    """
    image = await async_read(file_path=image_path)
    return await image_to_string(image=image, tesseract_path=tesseract_path, language=language, 
                                config=config, tesseract_single_threaded=tesseract_single_threaded, 
                                semaphore=semaphore)
