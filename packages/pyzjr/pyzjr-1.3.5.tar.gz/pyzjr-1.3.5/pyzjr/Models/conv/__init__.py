"""
收录或复现的其他改进的卷积
"""
from .Snake_Conv import DSConv
from .Depthwise_Conv import DepthSepConv, DWConv, PWConv
from .Partial_Conv import PartialConv
from .Ref_Conv import RefConv

__all__ = ["DSConv", "DepthSepConv", "PartialConv", "RefConv", "DWConv", "PWConv"]