"""
Copyright (c) 2024, Auorui.
All rights reserved.
time 2024-01-25
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from pyzjr.nn.torchutils.loss_utils import boundary_loss

__all__ = ["L1Loss", "L2Loss", "BCELoss", "CrossEntropyLoss", "FocalLoss", "DiceLoss"]

class L1Loss(nn.Module):
    """
    L1损失，也称为平均绝对误差（MAE），测量预测输出中的每个元素与目标或地面实况中的相应元素之间的平均绝对差。
    在数学上，它表示为预测值和目标值之间差异的绝对值的平均值。与L2损耗相比，L1损耗对异常值不那么敏感。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.
    Examples::
        >>> criterion1 = nn.L1Loss()
        >>> criterion2 = L1Loss()
        >>> input_data=torch.Tensor([2, 3, 4, 5])
        >>> target_data=torch.Tensor([4, 5, 6, 7])
        >>> loss1 = criterion1(input_data, target_data)  # tensor(2.)
        >>> loss2 = criterion2(input_data, target_data)  # tensor(2.)
    Returns:
        torch.Tensor: The L1 loss between input and target.
    """
    def __init__(self):
        super(L1Loss, self).__init__()

    def forward(self, input, target):
        loss = torch.mean(torch.abs(input - target))
        return loss

class L2Loss(nn.Module):
    """
    L2损失，也称为均方误差（MSE），测量预测输出中的每个元素与目标或地面实况中的相应元素之间的平均平方差。
    在数学上，它表示为预测值和目标值之间差异的平方的平均值。相比于L1损耗，L2损耗对异常值更敏感。依据公式实现。
    在torch当中是MSELoss
    Args:
        input (torch.Tensor): The predicted output.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.
    Examples::
        >>> criterion1 = nn.MSELoss()
        >>> criterion2 = L2Loss()
        >>> input_data=torch.Tensor([2, 3, 4, 5])
        >>> target_data=torch.Tensor([4, 5, 6, 7])
        >>> loss1 = criterion1(input_data, target_data)  # tensor(4.)
        >>> loss2 = criterion2(input_data, target_data)  # tensor(4.)

    Returns:
        torch.Tensor: The L2 loss between input and target.
    """
    def __init__(self):
        super(L2Loss, self).__init__()

    def forward(self, input, target):
        loss = torch.mean(torch.pow(input - target, 2))
        return loss

class BCELoss(nn.Module):
    """
    二元交叉熵损失（Binary Cross Entropy Loss），也称为对数损失。
    用于测量预测输出中的每个元素与目标或地面实况中的相应元素之间的对数概率差异。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output.Map to (0,1) through sigmoid function.
        target (torch.Tensor): The target or ground truth.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion1 = nn.BCELoss()
        >>> criterion2 = BCELoss()
        >>> input_data = torch.randn((5,))
        >>> target_data = torch.randint(0, 2, (5,), dtype=torch.float32)
        >>> loss1 = criterion1(torch.sigmoid(input_data), target_data)
        >>> loss2 = criterion2(input_data, target_data)
        >>> print("PyTorch BCELoss:", loss1.item())
        >>> print("Custom BCELoss:", loss2.item())

    Returns:
        torch.Tensor: The binary cross entropy loss between input and target.
    """
    def __init__(self, ignore_index=None, reduction='mean'):
        super(BCELoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        input = torch.sigmoid(input)
        loss = - (target * torch.log(input) + (1 - target) * torch.log(1 - input))
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss

class CrossEntropyLoss(nn.Module):
    """
    交叉熵损失（Cross Entropy Loss）用于多分类问题。
    用于测量预测输出和目标分布之间的交叉熵。依据公式实现。
    Args:
        input (torch.Tensor): The predicted output (logits).
        target (torch.Tensor): The target or ground truth (class labels).
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion1 = nn.CrossEntropyLoss()
        >>> criterion2 = CrossEntropyLoss()
        >>> input_data = torch.randn((3, 5), requires_grad=True)
        >>> target_data = torch.randint(0, 5, (3,))
        >>> loss1 = criterion1(input_data, target_data)
        >>> loss2 = criterion2(input_data, target_data)
        >>> print("PyTorch CrossEntropyLoss:", loss1.item())
        >>> print("Custom CrossEntropyLoss:", loss2.item())

    Returns:
        torch.Tensor: The cross entropy loss between input and target.
    """
    def __init__(self, ignore_index=None, reduction='mean'):
        super(CrossEntropyLoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        return nn.NLLLoss(reduction=self.reduction)(F.log_softmax(input, dim=1), target)


class FocalLoss(nn.Module):
    """
    Focal Loss 用于解决类别不平衡问题，通过缩小易分类的类别的损失来关注难分类的类别。依据公式实现。

    Args:
        alpha (float, optional): 控制易分类的类别的权重，大于1表示增加权重，小于1表示减小权重。默认为1.
        gamma (float, optional): 控制难分类的类别的损失的下降速度，大于0表示下降较慢，小于0表示下降较快。默认为2.
        reduction (str, optional): Specifies the reduction to apply to the output.
            Options are 'none', 'mean', or 'sum'. Default is 'mean'.

    Examples::
        >>> criterion = FocalLoss(alpha=1, gamma=2, reduction='mean')
        >>> input_data = torch.randn((5, 3), requires_grad=True)
        >>> target_data = torch.randint(0, 3, (5,))
        >>> loss = criterion(input_data, target_data)
        >>> print("Focal Loss:", loss.item())
    """
    def __init__(self, alpha=1, gamma=2, ignore_index=None, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        ce_loss = F.cross_entropy(input, target, reduction='none')
        class_weights = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - class_weights) ** self.gamma * ce_loss
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        elif self.reduction == 'none':
            return focal_loss

class DiceLoss(nn.Module):
    """
    Dice Loss 测量预测的和目标的二进制分割掩码之间的不相似性。它被计算为1减去Dice系数，Dice系数是重叠的度量
    在预测区域和目标区域之间。

    Examples::
        >>> criterion = DiceLoss(reduction='mean')
        >>> predictions = torch.rand((1,2,16,16), dtype=torch.float32)
        >>> targets = torch.randn((1,2,16,16), dtype=torch.float32)
        >>> loss = criterion(predictions, targets)
        >>> print("Dice Loss:", loss.item())

    Returns:
        torch.Tensor: The Dice Loss between input and target.
    """
    def __init__(self, ignore_index=None, reduction='mean', eps=1e-5):
        super(DiceLoss, self).__init__()
        self.eps = eps
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]

        input = torch.sigmoid(input)
        intersection = torch.sum(input * target)
        union = torch.sum(input) + torch.sum(target)
        dice_loss = 1 - (2 * intersection + self.eps) / (union + self.eps)
        if self.reduction == 'mean':
            return dice_loss.mean()
        elif self.reduction == 'sum':
            return dice_loss.sum()
        elif self.reduction == 'none':
            return dice_loss


class BoundaryLoss(nn.Module):
    """
    计算二进制分割的边界损失

    Args:
        None

    Examples:
        >>> criterion = BoundaryLoss()
        >>> outputs_soft = torch.rand((1, 1, 3, 3))  # model prediction
        >>> outputs_soft = torch.sigmoid(outputs_soft)
        >>> label_batch = torch.randint(2, (1, 1, 3, 3))  # binary segmentation mask
        >>> loss = criterion(outputs_soft, label_batch)
        >>> print("Boundary Loss:", loss.item())
    Returns:
        torch.Tensor: The Boundary Loss between model predictions and ground truth.
    """
    def __init__(self, ignore_index=None, reduction='mean'):
        super(BoundaryLoss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:,:self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        loss = boundary_loss(input, target)
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss

class LabelSmoothingCrossEntropy(torch.nn.Module):
    def __init__(self, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing

    def forward(self, pred, target):
        confidence = 1. - self.smoothing
        log_probs = F.log_softmax(pred, dim=-1)
        idx = torch.stack([torch.arange(log_probs.shape[0]), target], dim=1)
        nll_loss = torch.gather(-log_probs, dim=-1, index=idx)
        smooth_loss = torch.mean(-log_probs, dim=-1)
        loss = confidence * nll_loss + self.smoothing * smooth_loss

        return loss.mean()


class Joint2loss(nn.Module):
    """
    联合损失函数, 传入两个损失函数
        >>> criterion1 = FocalLoss()
        >>> criterion2 = DiceLoss()
        >>> joint_loss = Joint2loss(criterion1, criterion2, alpha=0.7, reduction='mean')
        >>> input_tensor = torch.rand((1,2,16,16), dtype=torch.float32)
        >>> target_tensor = torch.randn((1,2,16,16), dtype=torch.float32)
        >>> loss = joint_loss(input_tensor, target_tensor)
        >>> print("Joint Loss:", loss.item())
    """
    def __init__(self, *args, alpha, beta=None, ignore_index=None, reduction='mean'):
        super(Joint2loss, self).__init__()
        self.reduction = reduction
        self.ignore_index = ignore_index
        self.alpha = alpha
        self.beta = beta if beta is not None else 1-self.alpha
        self.criterion_1, self.criterion_2 = args

    def forward(self, input, target):
        if self.ignore_index:
            input = input[:, :self.ignore_index,...]
            target = target[:, :self.ignore_index, ...]
        loss_1 = self.criterion_1(input, target)
        loss_2 = self.criterion_2(input, target)
        loss = self.alpha * loss_1 + self.beta * loss_2
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        elif self.reduction == 'none':
            return loss

if __name__=="__main__":
    criterion1 = FocalLoss()
    criterion2 = DiceLoss()
    joint_loss = Joint2loss(criterion1, criterion2, alpha=0.7, reduction='mean')
    input_tensor = torch.rand((4,2,16,16), dtype=torch.float32)
    target_tensor = torch.randn((4,2,16,16), dtype=torch.float32)
    loss = joint_loss(input_tensor, target_tensor)
    print("Joint Loss:", loss.item())