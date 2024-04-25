#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#---------------------------------------------------------------
# imports
#---------------------------------------------------------------
from termcolor import colored
import cv2
import os 
import gdown
import numpy as np
from typing import Tuple
#---------------------------------------------------------------
def LOG_INFO(msg: str, mcolor: str = 'blue') -> None:
    """
    Log information with colored output.

    Args:
        msg (str): Message to be logged.
        mcolor (str): Color for the log message (default is 'blue').
    """
    print(colored("#LOG     :", 'green') + colored(msg, mcolor))

#---------------------------------------------------------------
def create_dir(base: str, ext: str) -> str:
    """
    Create a directory if it doesn't exist.

    Args:
        base (str): Base directory.
        ext (str): Extension or subdirectory name.

    Returns:
        str: Path to the created directory.
    """
    _path = os.path.join(base, ext)
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path

#---------------------------------------------------------------
def download(id: str, save_dir: str) -> None:
    """
    Download a file using its ID to the specified directory.

    Args:
        id (str): File ID or URL for download.
        save_dir (str): Directory to save the downloaded file.

    """
    gdown.download(id=id, output=save_dir, quiet=False)

#---------------------------------------------------------------
class dotdict(dict):
    """
    A dictionary with dot notation for attribute access.

    Attributes:
        __getattr__: Get attribute using dot notation.
        __setattr__: Set attribute using dot notation.
        __delattr__: Delete attribute using dot notation.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

#-------------------------
# crop processing helpers
#------------------------

def padWordImage(img: np.ndarray, pad_loc: str, pad_dim: int, pad_val: int) -> np.ndarray:
    """
    Pad the word image based on specified padding location and dimensions.

    Args:
        img (numpy.ndarray): Input image.
        pad_loc (str): Location for padding, 'lr' for left-right or 'tb' for top-bottom.
        pad_dim (int): Dimension for padding.
        pad_val (int): Padding value.

    Returns:
        numpy.ndarray: Padded image.
    """    
    if pad_loc == "lr":
        # Padding on left-right (horizontal)
        h, w, d = img.shape
        # Calculate pad widths
        pad_width = pad_dim - w
        # Create the pad
        pad = np.ones((h, pad_width, 3)) * pad_val
        # Concatenate the pad to the image
        img = np.concatenate([img, pad], axis=1)
    else:
        # Padding on top-bottom (vertical)
        h, w, d = img.shape
        # Calculate pad heights
        if h >= pad_dim:
            return img
        else:
            pad_height = pad_dim - h
            # Create the pad
            pad = np.ones((pad_height, w, 3)) * pad_val
            # Concatenate the pad to the image
            img = np.concatenate([img, pad], axis=0)
    return img.astype("uint8")    
#---------------------------------------------------------------
def correctPadding(img: np.ndarray, dim: Tuple[int, int], pvalue: int = 255) -> Tuple[np.ndarray, int]:
    """
    Correct the padding of the word image based on the specified dimensions.

    Args:
        img (numpy.ndarray): Input image.
        dim (Tuple[int, int]): Desired dimensions (height, width).
        pvalue (int): Padding value.

    Returns:
        tuple: Resized and padded image, mask indicating the width after padding.
    """    
    img_height, img_width = dim
    mask = 0
    
    # Check for padding
    h, w, d = img.shape
    
    # Resize image based on aspect ratio
    w_new = int(img_height * w / h)
    img = cv2.resize(img, (w_new, img_height))
    h, w, d = img.shape
    
    if w > img_width:
        # For larger width, resize based on aspect ratio
        h_new = int(img_width * h / w)
        img = cv2.resize(img, (img_width, h_new))
        # Pad the image (top-bottom)
        img = padWordImage(img, pad_loc="tb", pad_dim=img_height, pad_val=pvalue)
        mask = img_width
    elif w < img_width:
        # Pad the image (left-right)
        img = padWordImage(img, pad_loc="lr", pad_dim=img_width, pad_val=pvalue)
        mask = w
    
    # Resize the image to the desired dimensions
    img = cv2.resize(img, (img_width, img_height))
    
    return img, mask