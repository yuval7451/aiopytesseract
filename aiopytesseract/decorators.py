"""
Author
------
- Yuval Kaneti

Purpose
-------
- Decorators For aiopytesseract.
"""

## Imports
import time
import warnings
warnings.filterwarnings("always", category=DeprecationWarning, module=__name__)
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, Coroutine

from .utils import LoggingFactory
from .common import DEBUG, DEPRECATION_WARNING_EXCHANGE, DEPRECATION_WARNING, STACKLEVEL

Logger = LoggingFactory(__name__)

## Functions
def async_performance(func: Callable[..., Any]) -> Callable[..., Coroutine]:
    """async_performance: A Decorator for measuring async performance. 
    Parameters
    ----------
    func : Callable[..., Any]
        A Callable Function.

    Returns
    -------
    Callable[..., Coroutine]
        The Callble function output.
    """    
    @wraps(func)
    async def _performance(*args, **kwargs):
        if DEBUG:
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            Logger.debug(f"Function <{func.__name__}> took {end - start} Seconds to Execute")
            return result
        else:
            return await func(*args, **kwargs)
    return _performance


def sync_performance(func: Callable[..., Any]) -> Callable[..., Any]:
    """sync_performance: A Decorator for measuring sync performance. 
    Parameters
    ----------
    func : Callable[..., Any]
        A Callable Function.

    Returns
    -------
    Callable[..., Coroutine]
        The Callble function output.
    """    
    @wraps(func)
    def _performance(*args, **kwargs):
        if DEBUG:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            Logger.debug(f"Function <{func.__name__}> took {end - start} Seconds to Execute")
            return result
        else:
            return func(*args, **kwargs)
    return _performance


def deprecated(func: Callable[..., Any]) -> Callable[..., Any]:
    """deprecated: A Decorator for warning about depraceted functions. 
    Parameters
    ----------
    func : Callable[..., Any]
        A Callable Function.

    Returns
    -------
    Callable[..., Coroutine]
        The Callble function output.
    """   
    @wraps(func)
    def _deprecated(*args, **kwargs):       
        warnings.warn(DEPRECATION_WARNING.format(func.__name__), DeprecationWarning, stacklevel=STACKLEVEL)
        return func(*args, **kwargs)
    
    @wraps(func)
    async def _async_deprecated(*args, **kwargs):       
        warnings.warn(DEPRECATION_WARNING.format(func.__name__), DeprecationWarning, stacklevel=STACKLEVEL)  
        return await func(*args, **kwargs)
 
    return _async_deprecated if iscoroutinefunction(func) else _deprecated


def deprecated_exchange(exchnage: Callable[..., Any]) -> Callable[..., Any]:
    """deprecated_exchange: A Decorator for warning about depraceted functions and suggesting a Diffrent functions should be used. 
    Parameters
    ----------
    func : Callable[..., Any]
        A Callable Function.

    Returns
    -------
    Callable[..., Coroutine]
        The Callble function output.
    """  
    def _deprecated_exchange(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def _deprecated(*args, **kwargs): 
            warnings.warn(DEPRECATION_WARNING_EXCHANGE.format(func.__name__, exchnage.__name__), DeprecationWarning, stacklevel=STACKLEVEL)
            return func(*args, **kwargs)
        
        @wraps(func)
        async def _async_deprecated(*args, **kwargs):       
            warnings.warn(DEPRECATION_WARNING_EXCHANGE.format(func.__name__, exchnage.__name__), DeprecationWarning, stacklevel=STACKLEVEL)  
            return await func(*args, **kwargs)
    
        return _async_deprecated if iscoroutinefunction(func) else _deprecated

    return _deprecated_exchange