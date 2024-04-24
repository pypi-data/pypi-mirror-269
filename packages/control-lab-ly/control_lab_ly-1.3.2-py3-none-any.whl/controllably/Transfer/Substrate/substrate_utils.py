# %% -*- coding: utf-8 -*-
"""
This module holds the base class for substrate gripper tools.

Classes:
    Gripper (ABC)
"""
# Standard library imports
from abc import ABC, abstractmethod
print(f"Import: OK <{__name__}>")

class Gripper(ABC):
    """
    Abstract Base Class (ABC) for Gripper objects (i.e. tools that picks up and places objects).
    ABC cannot be instantiated, and must be subclassed with abstract methods implemented before use.

    ### Methods
    #### Abstract
    - `drop`: releases an object
    - `grab`: picks up an object
    #### Public
    - `toggleGrip`: grip or release the object
    """
    
    def __init__(self):
        """Instantiate the class"""
        ...
    
    @abstractmethod
    def drop(self) -> bool:
        """
        Releases an object
        
        Returns:
            bool: whether action is successful
        """
    
    @abstractmethod
    def grab(self) -> bool:
        """
        Picks up an object
        
        Returns:
            bool: whether action is successful
        """
    
    def toggleGrip(self, on:bool):
        """
        Grip or release the object

        Args:
            on (bool): whether to grip the object
        """
        if on:
            self.grab()
        else:
            self.drop()
        return
