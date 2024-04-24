# %% -*- coding: utf-8 -*-
"""
This module holds the base class for image data.

Functions:
    addText
    annotate
    blur
    convolve
    crosshair
    process
    removeNoise
    rotate
"""
# Standard library imports
from __future__ import annotations
import numpy as np

# Third party imports
import cv2              # pip install opencv-python
print(f"Import: OK <{__name__}>")
    
def addText(frame:np.ndarray, text:str, position:tuple[int]) -> np.ndarray:
    """
    Add text to the image

    Args:
        frame (np.ndarray): frame array
        text (str): text to be added
        position (tuple[int]): x,y position of where to place the text

    Returns:
        np.ndarray: frame array
    """
    return cv2.putText(frame, text, position, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)

def annotate(frame:np.ndarray, index:int, dimensions:tuple[int]) -> np.ndarray:
    """
    Annotate the image to label identified targets

    Args:
        frame (np.ndarray): frame array
        index (int): index of target
        dimensions (tuple[int]): list of x,y,w,h

    Returns:
        np.ndarray: frame array
    """
    x,y,w,h = dimensions
    frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    frame = cv2.circle(frame, (int(x+(w/2)), int(y+(h/2))), 3, (0,0,255), -1)
    frame = cv2.putText(frame, '{}'.format(index+1), (x-8, y-4), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
    return frame

def blur(frame:np.ndarray, blur_kernel:int = 3) -> np.ndarray:
    """
    Blur the image

    Args:
        frame (np.ndarray): frame array
        blur_kernel (int, optional): level of blurring, odd numbers only, minimum value of 3. Defaults to 3.

    Returns:
        np.ndarray: frame array
    """
    return cv2.GaussianBlur(frame, (blur_kernel,blur_kernel), 0)

def convolve(frame:np.ndarray) -> np.ndarray: # FIXME
    """
    Perform convolution on image

    Args:
        frame (np.ndarray): frame array

    Returns:
        np.ndarray: frame array
    """
    return

def crosshair(frame:np.ndarray) -> np.ndarray:
    """
    Add crosshair in the middle of image

    Args:
        frame (np.ndarray): frame array

    Returns:
        np.ndarray: frame array
    """
    center_x = int(frame.shape[1] / 2)
    center_y = int(frame.shape[0] / 2)
    cv2.line(frame, (center_x, center_y+50), (center_x, center_y-50), (255,255,255), 1)
    cv2.line(frame, (center_x+50, center_y), (center_x-50, center_y), (255,255,255), 1)
    return frame

def process(frame:np.ndarray, alpha:float, beta:float, blur_kernel:int = 3) -> np.ndarray: # FIXME
    """
    Process the image

    Args:
        frame (np.ndarray): frame array
        alpha (float): alpha value
        beta (float): beta value
        blur_kernel (int, optional): level of blurring, odd numbers only, minimum value of 3. Defaults to 3.

    Returns:
        np.ndarray: frame array
    """
    frame = cv2.addWeighted(frame, alpha, np.zeros(frame.shape, frame.dtype), 0, beta)
    if blur_kernel > 0:
        frame = cv2.GaussianBlur(frame, (blur_kernel,blur_kernel), 0)
    return frame

def removeNoise(frame:np.ndarray, open_iter:int = 0, close_iter:int = 0) -> np.ndarray:
    """
    Remove noise from image

    Args:
        frame (np.ndarray): frame array
        open_iter (int, optional): opening iteration. Defaults to 0.
        close_iter (int, optional): closing iteration. Defaults to 0.

    Returns:
        np.ndarray: frame array
    """
    kernel = np.ones((3,3),np.uint8)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.morphologyEx(frame,cv2.MORPH_OPEN,kernel,iterations=open_iter)
    frame = cv2.morphologyEx(frame,cv2.MORPH_CLOSE,kernel,iterations=close_iter)
    return frame

def rotate(frame:np.ndarray, angle:int) -> np.ndarray:
    """
    Rotate a 2D array of multiples of 90 degrees, clockwise

    Args:
        frame (np.ndarray): frame array
        angle (int): 90, 180, or 270 degrees

    Returns:
        np.ndarray: frame array
    """
    rotateCodes = {
        90: cv2.ROTATE_90_CLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE
    }
    if angle != 0:
        frame = cv2.rotate(frame, rotateCodes.get(angle))
    return frame

__where__ = "View.Image"
from controllably import include_this_module
include_this_module(get_local_only=True)

# NOTE: DEPRECATED

# class Image:
#     """
#     Image class with image manipulation methods

#     ### Constructor
#     Args:
#         `frame` (np.ndarray): frame array
        
#     ### Attributes
#     - `frame` (np.ndarray): frame array
    
#     ### Methods
#     - `addText`: add text to the image
#     - `annotate`: annotate the image to label identified targets
#     - `blur`: blur the image
#     - `convertToRGB`: turn the image to RGB
#     - `crosshair`: add crosshair in the middle of image
#     - `encode`: encode the frame into bytes
#     - `grayscale`: turn image to grayscale
#     - `process`: process the image
#     - `removeNoise`: remove noise from image
#     - `resize`: resize the image
#     - `rotate`: rotate the 2D array of multiples of 90 degrees, clockwise
#     - `save`: save image to file
#     """
    
#     def __init__(self, frame:np.ndarray):
#         """
#         Instantiate the class

#         Args:
#             frame (np.ndarray): frame array
#         """
#         self.frame = frame
#         pass
    
#     def addText(self, text:str, position:tuple[int], inplace:bool = False) -> Optional[Image]:
#         """
#         Add text to the image

#         Args:
#             text (str): text to be added
#             position (tuple[int]): x,y position of where to place the text
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = self.frame
#         frame = cv2.putText(frame, text, position, cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def annotate(self, index:int, dimensions:tuple[int], inplace:bool = False) -> Optional[Image]:
#         """
#         Annotate the image to label identified targets

#         Args:
#             index (int): index of target
#             dimensions (tuple[int]): list of x,y,w,h
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         x,y,w,h = dimensions
#         frame = self.frame
#         frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
#         frame = cv2.circle(frame, (int(x+(w/2)), int(y+(h/2))), 3, (0,0,255), -1)
#         frame = cv2.putText(frame, '{}'.format(index+1), (x-8, y-4), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def blur(self, blur_kernel:int = 3, inplace:bool = False) -> Optional[Image]:
#         """
#         Blur the image

#         Args:
#             blur_kernel (int, optional): level of blurring, odd numbers only, minimum value of 3. Defaults to 3.
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = cv2.GaussianBlur(self.frame, (blur_kernel,blur_kernel), 0)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def convertToRGB(self, inplace:bool = False) -> Optional[Image]:
#         """
#         Turn image to RGB

#         Args:
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     # def convolve(self, inplace:bool = False) -> Optional[Image]: # FIXME
#     #     """
#     #     Perform convolution on image

#     #     Args:
#     #         inplace (bool, optional): whether to perform action in place. Defaults to False.

#     #     Returns:
#     #         Image, or None: Image object, or None (if inplace=True)
#     #     """
#     #     return
    
#     def crosshair(self, inplace:bool = False) -> Optional[Image]:
#         """
#         Add crosshair in the middle of image

#         Args:
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = self.frame
#         center_x = int(frame.shape[1] / 2)
#         center_y = int(frame.shape[0] / 2)
#         cv2.line(frame, (center_x, center_y+50), (center_x, center_y-50), (255,255,255), 1)
#         cv2.line(frame, (center_x+50, center_y), (center_x-50, center_y), (255,255,255), 1)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def encode(self, extension:str = '.png'):
#         """
#         Encode image into byte array

#         Args:
#             extension (str, optional): image format to encode to. Defaults to '.png'.

#         Returns:
#             bytes: byte array of image
#         """
#         return cv2.imencode(extension, self.frame)[1].tobytes()
    
#     def grayscale(self, inplace:bool = False) -> Optional[Image]:
#         """
#         Turn image to grayscale

#         Args:
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def process(self, alpha:float, beta:float, blur_kernel:int = 3, inplace:bool = False) -> Optional[Image]: # FIXME
#         """
#         Process the image

#         Args:
#             alpha (float): alpha value
#             beta (float): beta value
#             blur_kernel (int, optional): level of blurring, odd numbers only, minimum value of 3. Defaults to 3.
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = self.frame
#         frame = cv2.addWeighted(frame, alpha, np.zeros(frame.shape, frame.dtype), 0, beta)
#         if blur_kernel > 0:
#             frame = cv2.GaussianBlur(frame, (blur_kernel,blur_kernel), 0)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def removeNoise(self, open_iter:int = 0, close_iter:int = 0, inplace:bool = False) -> Optional[Image]:
#         """
#         Remove noise from image

#         Args:
#             open_iter (int, optional): opening iteration. Defaults to 0.
#             close_iter (int, optional): closing iteration. Defaults to 0.
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         kernel = np.ones((3,3),np.uint8)
#         frame = self.frame
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         frame = cv2.morphologyEx(frame,cv2.MORPH_OPEN,kernel,iterations=open_iter)
#         frame = cv2.morphologyEx(frame,cv2.MORPH_CLOSE,kernel,iterations=close_iter)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def resize(self, size:tuple[int], inplace:bool = False) -> Optional[Image]:
#         """
#         Resize the image

#         Args:
#             size (tuple[int]): tuple of desired image width and height
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         frame = cv2.resize(self.frame, size)
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)
    
#     def rotate(self, angle:int, inplace:bool = False) -> Optional[Image]:
#         """
#         Rotate a 2D array of multiples of 90 degrees, clockwise

#         Args:
#             angle (int): 90, 180, or 270 degrees
#             inplace (bool, optional): whether to perform action in place. Defaults to False.

#         Returns:
#             Optional[Image]: None if inplace else `Image` object
#         """
#         rotateCodes = {
#             90: cv2.ROTATE_90_CLOCKWISE,
#             180: cv2.ROTATE_180,
#             270: cv2.ROTATE_90_COUNTERCLOCKWISE
#         }
#         frame = self.frame
#         if angle != 0:
#             frame = cv2.rotate(frame, rotateCodes.get(angle))
#         if inplace:
#             self.frame = frame
#             return
#         return Image(frame)

#     def save(self, filename:str):
#         """
#         Save image to file

#         Args:
#             filename (str): filename to save to

#         Returns:
#             bool: whether the image is successfully saved
#         """
#         return cv2.imwrite(filename, self.frame)


# def convertToRGB(frame:np.ndarray) -> np.ndarray:
#     """
#     Turn image to RGB

#     Args:
#         frame (np.ndarray): frame array

#     Returns:
#         np.ndarray: frame array
#     """
#     return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# def encode(frame:np.ndarray, extension:str = '.png') -> bytes:
#     """
#     Encode image into byte array

#     Args:
#         frame (np.ndarray): frame array
#         extension (str, optional): image format to encode to. Defaults to '.png'.

#     Returns:
#         bytes: byte array of image
#     """
#     return cv2.imencode(extension, frame)[1].tobytes()

# def grayscale(frame:np.ndarray) -> np.ndarray:
#     """
#     Turn image to grayscale

#     Args:
#         frame (np.ndarray): frame array

#     Returns:
#         np.ndarray: frame array
#     """
#     return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# def resize(frame:np.ndarray, size:tuple[int]) -> np.ndarray:
#     """
#     Resize the image

#     Args:
#         frame (np.ndarray): frame array
#         size (tuple[int]): tuple of desired image width and height

#     Returns:
#         np.ndarray: frame array
#     """
#     return cv2.resize(frame, size)

# def save(frame:np.ndarray, filename:str) -> bool:
#     """
#     Save image to file

#     Args:
#         frame (np.ndarray): frame array
#         filename (str): filename to save to

#     Returns:
#         bool: whether the image is successfully saved
#     """
#     return cv2.imwrite(filename, frame)
