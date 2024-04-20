import os
import torch
import gc

def Central_Processing_Unit():
    """
    Returns the CPU device.

    Returns:
        torch.device: The CPU device.
    """
    return torch.device('cpu')

def Graphics_Processing_Unit(i=0, cuda=True):
    """
    If cuda is true and gpu is available, return gpu (i); otherwise, return cpu()
    :param i: Index i, indicating which GPU block to use
    :param cuda: Boolean value indicating whether to use cuda, if not, CPU can be used, set to False
    """
    if cuda and torch.cuda.is_available() and torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

def use_all_gpu():
    """
    Those who can use this function must be very rich.
    """
    devices = []
    for i in range(torch.cuda.device_count()):
        devices.append(i)
    return devices if devices else [torch.device('cpu')]

def num_workers(batch_size):
    """
    Determine the number of parallel worker processes used for data loading
    """
    return min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])

def release_memory(*args):
    """
    Function to release memory resources, particularly useful when working with PyTorch and CUDA.
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    if not isinstance(args, list):
        args = list(args)
    for i in range(len(args)):
        args[i] = None
    gc.collect()
    return args


CPU = cpu = Central_Processing_Unit
GPU = gpu = Graphics_Processing_Unit


