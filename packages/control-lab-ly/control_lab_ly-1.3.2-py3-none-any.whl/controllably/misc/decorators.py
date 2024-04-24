# %% -*- coding: utf-8 -*-
"""
This module holds the decorator functions in Control.lab.ly.

Functions:
    safety_measures (decorator)
"""
# Standard library imports
from functools import wraps
import time
from typing import Callable, Optional
print(f"Import: OK <{__name__}>")

def safety_measures(mode:Optional[str] = None, countdown:int = 3) -> Callable:
    """
    Wrapper for creating safe move functions

    Args:
        mode (Optional[str], optional): mode for implementing safety measure. Defaults to None.
        countdown (int, optional): time delay before executing action. Defaults to 3.
        
    Returns:
        Callable: wrapped function
    """
    def inner(func:Callable) -> Callable:
        """
        Inner wrapper for creating safe move functions

        Args:
            func (Callable): function to be wrapped

        Returns:
            Callable: wrapped function
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            str_method = repr(func).split(' ')[1]
            str_args = ','.join([repr(a) for a in args[1:]])
            str_kwargs = ','.join([f'{k}={v}' for k,v in kwargs.items()])
            str_inputs = ','.join(filter(None, [str_args, str_kwargs]))
            str_call = f"{str_method}({str_inputs})"
            if mode == 'wait':
                print(f"Executing in {countdown} seconds:")
                print(str_call)
                time.sleep(countdown)
            elif mode == 'pause':
                print(f"Executing: {str_call}")
                time.sleep(0.1)
                input(f"Press 'Enter' to execute")
            return func(*args, **kwargs)
        return wrapper
    return inner
