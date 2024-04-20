import os
import torch

def save_models(model, epoch, save_dir, save_period=10):
    """Save model to given path
    Args:
        model: model to be saved
        save_dir: path that the model would be saved
        epoch: the epoch the model finished training
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if epoch % save_period == 0:
        torch.save(model.state_dict(), os.path.join(save_dir, f"model_epoch_{epoch}.pth"))

_torch_save = torch.save  # copy to avoid recursion errors

def torch_save(*args, **kwargs):
    """Use dill (if exists) to serialize the lambda functions where pickle does not do this.

    Args:
        *args (tuple): Positional arguments to pass to torch.save.
        **kwargs (dict): Keyword arguments to pass to torch.save.
    """
    try:
        import dill as pickle  # noqa
    except ImportError:
        import pickle
    if 'pickle_module' not in kwargs:
        kwargs['pickle_module'] = pickle  # noqa
    return _torch_save(*args, **kwargs)
