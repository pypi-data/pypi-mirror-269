import numpy as np
import re
from PIL import Image
import torch
import torch.nn as nn


def is_tensor(img):
    """Check if the input image is torch format."""
    return isinstance(img, torch.Tensor)

def is_pil(img):
    """Check if the input image is PIL format."""
    return isinstance(img, Image.Image)

def is_numpy(img):
    """Check if the input image is Numpy format."""
    return isinstance(img, np.ndarray)

def is_gray_image(image):
    return (len(image.shape) == 2) or (len(image.shape) == 3 and image.shape[-1] == 1)

def is_rgb_image(image):
    return len(image.shape) == 3 and image.shape[-1] == 3

def get_num_channels(image):
    return image.shape[2] if len(image.shape) == 3 else 1

def get_image_size(image):
    if is_numpy(image):
        h, w = image.shape[:2]
        return h, w
    if is_pil(image):
        w, h = image.size
        return h, w
    if is_tensor(image):
        if len(image.shape) == 4 or len(image.shape) == 3:
            w, h = image.shape[-2:]
            return h, w
    else:
        raise ValueError("[pyzjr]:Unsupported input type")

def get_image_num_channels(img):
    if is_tensor(img):
        if img.ndim == 2:
            return 1
        elif img.ndim > 2:
            return img.shape[-3]
    if is_pil(img):
        return 1 if img.mode == 'L' else 3
    if is_numpy(img):
        return 1 if is_gray_image else 3

def is_parallel(model):
    # Returns True if model is of type DP or DDP
    return isinstance(model, (nn.parallel.DataParallel, nn.parallel.DistributedDataParallel))

def is_int(param):
    return isinstance(param, int)

def is_float(param):
    return isinstance(param, float)

def is_list(param):
    return isinstance(param, list)

def is_tuple(param):
    return isinstance(param, tuple)

def is_list_or_tuple(param):
    return isinstance(param, (list, tuple))

def is_None(param):
    return True if param is None else False

def is_positive_int(param):
    return is_int(param) and param > 0

def is_nonnegative_int(param):
    return is_int(param) and param >= 0

def is_ascii(s):
    """
    Check if the string is composed of only ASCII characters.
    Args:
        s (str): String to be checked.
    Returns:
        bool: True if the string is composed only of ASCII characters, False otherwise.
    """
    s = str(s)
    return all(ord(c) < 128 for c in s)

def is_url(filename):
    """Return True if string is an http or ftp path."""
    URL_REGEX = re.compile(r'http://|https://|ftp://|file://|file:\\')
    return (isinstance(filename, str) and
            URL_REGEX.match(filename) is not None)