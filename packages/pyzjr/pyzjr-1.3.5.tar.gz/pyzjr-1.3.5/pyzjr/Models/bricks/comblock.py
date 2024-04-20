"""
Time: 2024-01-28 0:59
"""
import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from pyzjr.Models.attention import BAMAttention, SEAttention

def conv3x3(in_channels, out_channels, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding:捕捉局部特征和空间相关性，学习更复杂的特征和抽象表示"""
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride,
                     padding=dilation, groups=groups, bias=False, dilation=dilation)

def conv1x1(in_channels, out_channels, stride=1):
    """1x1 convolution:实现降维或升维，调整通道数和执行通道间的线性变换"""
    return nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False)

class ConvBNReLU(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1,  kernel_size=3, padding=1,
                 **kwargs):
        super(ConvBNReLU, self).__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                              kernel_size=kernel_size, stride=stride, padding=padding,
                              **kwargs)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

class ConvBNActivation(nn.Module):
    def __init__(self, in_planes, out_planes, kernel_size=3, stride=1, groups=1,
                 norm_layer=None, activation_layer = None, dilation=1,):
        super(ConvBNActivation, self).__init__()
        padding = (kernel_size - 1) // 2 * dilation
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        if activation_layer is None:
            activation_layer = nn.ReLU6
        self.convbnact=nn.Sequential(
            nn.Conv2d(in_planes, out_planes, kernel_size, stride, padding, dilation=dilation, groups=groups,
                      bias=False),
            norm_layer(out_planes),
            activation_layer(inplace=True)
        )
        self.out_channels = out_planes

    def forward(self, x):
        return self.convbnact(x)

class ConvBN(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1,  kernel_size=3, padding=1,
                 **kwargs):
        super(ConvBN, self).__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                              kernel_size=kernel_size, stride=stride, padding=padding,
                              **kwargs)
        self.bn = nn.BatchNorm2d(num_features=out_channels)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        return x

class BasicBlock(nn.Module):
    """ResNet的基础块,适用于较浅的网络或较小的数据集"""
    expansion = 1
    def __init__(self, in_channels, out_channels, stride=1, downsample=False):
        super(BasicBlock, self).__init__()
        self.convbnrelu = ConvBNReLU(in_channels, out_channels, kernel_size=3, stride=stride)
        self.convbn = ConvBN(out_channels, out_channels, kernel_size=3)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride
        self.conv_down = nn.Sequential(
            conv1x1(in_channels, out_channels * self.expansion, self.stride),
            nn.BatchNorm2d(out_channels * self.expansion),
        )

    def forward(self, x):
        residual = x
        out = self.convbnrelu(x)
        out = self.convbn(out)

        if self.downsample:
            residual = self.conv_down(x)

        out += residual
        out = self.relu(out)

        return out

class SPBlock(nn.Module):
    """引入条形池化的思想"""
    def __init__(self, inplanes, outplanes, norm_layer=None):
        super(SPBlock, self).__init__()
        midplanes = outplanes
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self.conv1 = nn.Conv2d(inplanes, midplanes, kernel_size=(3, 1), padding=(1, 0), bias=False)
        self.bn1 = norm_layer(midplanes)
        self.conv2 = nn.Conv2d(inplanes, midplanes, kernel_size=(1, 3), padding=(0, 1), bias=False)
        self.bn2 = norm_layer(midplanes)
        self.conv3 = nn.Conv2d(midplanes, outplanes, kernel_size=1, bias=True)
        self.pool1 = nn.AdaptiveAvgPool2d((None, 1))
        self.pool2 = nn.AdaptiveAvgPool2d((1, None))
        self.relu = nn.ReLU(inplace=False)

    def forward(self, x):
        _, _, h, w = x.size()
        x1 = self.pool1(x)
        x1 = self.conv1(x1)
        x1 = self.bn1(x1)
        x1 = x1.expand(-1, -1, h, w)
        #x1 = F.interpolate(x1, (h, w))

        x2 = self.pool2(x)
        x2 = self.conv2(x2)
        x2 = self.bn2(x2)
        x2 = x2.expand(-1, -1, h, w)
        #x2 = F.interpolate(x2, (h, w))

        x = self.relu(x1 + x2)
        x = self.conv3(x).sigmoid()
        return x

class Bottleneck(nn.Module):
    """ResNet的瓶颈结构,适用于深层网络，通过较少的参数来构建更深的网络，提高性能"""
    expansion = 4
    def __init__(self, in_channels, out_channels, stride=1, downsample=False):
        super(Bottleneck, self).__init__()
        groups = 1
        base_width = 64
        dilation = 1

        width = int(out_channels * (base_width / 64.)) * groups   # wide = out_channels
        # self.convbnrelu1 = ConvBNReLU(in_channels, width, kernel_size=1, padding=0)  # 降维通道数
        # self.convbnrelu2 = ConvBNReLU(width, width, kernel_size=3, stride=stride, dilation=dilation, groups=groups)
        # self.convbn3 = ConvBN(width, out_channels * self.expansion, kernel_size=1, padding=0)   # 升维通道数
        self.conv1 = conv1x1(in_channels, width)       # 降维通道数
        self.bn1 = nn.BatchNorm2d(width)
        self.conv2 = conv3x3(width, width, stride, groups, dilation)
        self.bn2 = nn.BatchNorm2d(width)
        self.conv3 = conv1x1(width, out_channels * self.expansion)   # 升维通道数
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride
        self.conv_down = nn.Sequential(
            conv1x1(in_channels, out_channels * self.expansion, self.stride),
            nn.BatchNorm2d(out_channels * self.expansion),
        )

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        # out = self.convbnrelu1(x)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        # out = self.convbnrelu2(out)
        out = self.conv3(out)
        out = self.bn3(out)
        # out = self.convbn3(out)
        if self.downsample:
            residual = self.conv_down(x)

        out += residual
        out = self.relu(out)

        return out

class FireModule(nn.Module):
    """对通道的压缩和扩展(SqueezeNet)"""
    def __init__(self, inplanes, squeeze_planes, expand1x1_planes, expand3x3_planes):
        super(FireModule, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes,
                                   kernel_size=1)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes,
                                   kernel_size=3, padding=1)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.relu(self.squeeze(x))
        return torch.cat([
            self.relu(self.expand1x1(x)),
            self.relu(self.expand3x3(x))
        ], dim=1)

class _DenseLayer(nn.Sequential):
    def __init__(self, num_input_features, growth_rate, bn_size, drop_rate):
        super(_DenseLayer, self).__init__()
        self.add_module('norm1', nn.BatchNorm2d(num_input_features)),
        self.add_module('relu1', nn.ReLU(inplace=True)),
        self.add_module('conv1', nn.Conv2d(num_input_features, bn_size *
                                           growth_rate, kernel_size=(1,1), stride=(1,1), bias=False)),
        self.add_module('norm2', nn.BatchNorm2d(bn_size * growth_rate)),
        self.add_module('relu2', nn.ReLU(inplace=True)),
        self.add_module('conv2', nn.Conv2d(bn_size * growth_rate, growth_rate,
                                           kernel_size=3, stride=(1,1), padding=1, bias=False)),
        self.drop_rate = drop_rate

    def forward(self, x):
        new_features = super(_DenseLayer, self).forward(x)
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        return torch.cat([x, new_features], 1)


class _DenseBlock(nn.Sequential):
    def __init__(self, num_layers, num_input_features, bn_size, growth_rate, drop_rate):
        super(_DenseBlock, self).__init__()
        for i in range(num_layers):
            layer = _DenseLayer(num_input_features + i * growth_rate, growth_rate, bn_size, drop_rate)
            self.add_module('denselayer%d' % (i + 1), layer)

class Transition(nn.Sequential):
    """
    减少通道数, 特征图尺寸减半, Densenet过渡层
    Densenet Transition Layer:
        1 × 1 conv
        2 × 2 average pool, stride 2
    """
    def __init__(self, num_input_features, num_output_features):
        super(Transition, self).__init__()
        self.norm = nn.BatchNorm2d(num_input_features)
        self.relu = nn.ReLU(inplace=True)
        self.conv = nn.Conv2d(num_input_features, num_output_features, kernel_size=1, stride=1, bias=False)
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)


class InvertedResidualv2(nn.Module):
    """MobileNetV2的倒残差结构"""
    def __init__(self, in_planes, out_planes, stride, expand_ratio):
        super(InvertedResidualv2, self).__init__()
        self.stride = stride
        assert stride in [1, 2]

        hidden_dim = int(round(in_planes * expand_ratio))
        self.use_res_connect = self.stride == 1 and in_planes == out_planes

        layers = []
        if expand_ratio != 1:
            # pw 利用1x1卷积进行通道数的上升
            layers.append(ConvBNActivation(in_planes, hidden_dim, kernel_size=1))
        layers.extend([
            # dw 进行3x3的逐层卷积，进行跨特征点的特征提取
            ConvBNActivation(hidden_dim, hidden_dim, stride=stride, groups=hidden_dim),
            # pw-linear 利用1x1卷积进行通道数的下降
            nn.Conv2d(hidden_dim, out_planes, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(out_planes),
        ])
        self.conv = nn.Sequential(*layers)
        self.out_channels = out_planes

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)


class GhostModulev1(nn.Module):
    def __init__(self, inp, oup, kernel_size=1, ratio=2, dw_size=3, stride=1, relu=True):
        super(GhostModulev1, self).__init__()
        self.oup = oup
        init_channels = math.ceil(oup / ratio)   # m = n / s
        new_channels = init_channels*(ratio-1)   # m * (s - 1) = n / s * (s - 1)

        # 利用1x1卷积对输入进来的特征图进行通道的浓缩, 实现跨通道的特征提取
        self.primary_conv = nn.Sequential(
            nn.Conv2d(inp, init_channels, kernel_size, stride, kernel_size//2, bias=False),
            nn.BatchNorm2d(init_channels),
            nn.ReLU(inplace=True) if relu else nn.Sequential(),
        )
        # 使用逐层卷积, 获得额外的特征图
        self.cheap_operation = nn.Sequential(
            nn.Conv2d(init_channels, new_channels, dw_size, stride=1, padding=dw_size//2, groups=init_channels, bias=False),
            nn.BatchNorm2d(new_channels),
            nn.ReLU(inplace=True) if relu else nn.Sequential(),
        )

    def forward(self, x):
        x1 = self.primary_conv(x)
        x2 = self.cheap_operation(x1)
        out = torch.cat([x1, x2], dim=1)
        return out[:, :self.oup, :, :]


class GhostBottleneckv1(nn.Module):
    """ Ghost bottleneck w/removed SE """
    def __init__(self, in_chs, mid_chs, out_chs, dw_size=3, stride=1):
        super(GhostBottleneckv1, self).__init__()
        self.stride = stride
        # Point-wise expansion
        self.ghost1 = GhostModulev1(in_chs, mid_chs, relu=True)
        # Depth-wise convolution
        if self.stride > 1:
            self.conv_dw = nn.Conv2d(mid_chs, mid_chs, dw_size, stride=stride,
                                     padding=(dw_size-1)//2,
                                     groups=mid_chs, bias=False)
            self.bn_dw = nn.BatchNorm2d(mid_chs)
        # Point-wise linear projection
        self.ghost2 = GhostModulev1(mid_chs, out_chs, relu=False)
        # shortcut
        if (in_chs == out_chs and self.stride == 1):
            self.shortcut = nn.Sequential()
        else:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_chs, in_chs, dw_size, stride=stride,
                          padding=(dw_size-1)//2, groups=in_chs, bias=False),
                nn.BatchNorm2d(in_chs),
                nn.Conv2d(in_chs, out_chs, 1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_chs),
            )

    def forward(self, x):
        residual = x
        # 1st ghost bottleneck
        x = self.ghost1(x)
        # Depth-wise convolution
        if self.stride > 1:
            x = self.conv_dw(x)
            x = self.bn_dw(x)
        # 2nd ghost bottleneck
        x = self.ghost2(x)
        x += self.shortcut(residual)
        return x


class GhostModulev2(nn.Module):
    """添加了DFC注意力机制,即short_conv部分,原文使用的是max_pool,这里使用的是avg_pool"""
    def __init__(self, inp, oup, kernel_size=1, ratio=2, dw_size=3, stride=1, relu=True, mode=None):
        super(GhostModulev2, self).__init__()
        self.mode = mode
        self.gate_fn = nn.Sigmoid()

        if self.mode in ['original']:
            self.oup = oup
            init_channels = math.ceil(oup / ratio)
            new_channels = init_channels*(ratio-1)
            self.primary_conv = nn.Sequential(
                nn.Conv2d(inp, init_channels, kernel_size, stride, kernel_size//2, bias=False),
                nn.BatchNorm2d(init_channels),
                nn.ReLU(inplace=True) if relu else nn.Sequential(),
            )
            self.cheap_operation = nn.Sequential(
                nn.Conv2d(init_channels, new_channels, dw_size, 1, dw_size//2, groups=init_channels, bias=False),
                nn.BatchNorm2d(new_channels),
                nn.ReLU(inplace=True) if relu else nn.Sequential(),
            )
        elif self.mode in ['attn']:
            self.oup = oup
            init_channels = math.ceil(oup / ratio)
            new_channels = init_channels*(ratio-1)
            self.primary_conv = nn.Sequential(
                nn.Conv2d(inp, init_channels, kernel_size, stride, kernel_size//2, bias=False),
                nn.BatchNorm2d(init_channels),
                nn.ReLU(inplace=True) if relu else nn.Sequential(),
            )
            self.cheap_operation = nn.Sequential(
                nn.Conv2d(init_channels, new_channels, dw_size, 1, dw_size//2, groups=init_channels, bias=False),
                nn.BatchNorm2d(new_channels),
                nn.ReLU(inplace=True) if relu else nn.Sequential(),
            )
            self.short_conv = nn.Sequential(
                # horizontal DFC and vertical DFC
                nn.Conv2d(inp, oup, kernel_size, stride, kernel_size//2, bias=False),
                nn.BatchNorm2d(oup),
                nn.Conv2d(oup, oup, kernel_size=(1, 5), stride=1, padding=(0,2), groups=oup,bias=False),
                nn.BatchNorm2d(oup),
                nn.Conv2d(oup, oup, kernel_size=(5, 1), stride=1, padding=(2,0), groups=oup,bias=False),
                nn.BatchNorm2d(oup),
            )

    def forward(self, x):
        if self.mode in ['original']:
            x1 = self.primary_conv(x)
            x2 = self.cheap_operation(x1)
            out = torch.cat([x1, x2], dim=1)
            return out[:, : self.oup, :, :]
        elif self.mode in ['attn']:
            res = self.short_conv(F.avg_pool2d(x, kernel_size=2, stride=2))
            x1 = self.primary_conv(x)
            x2 = self.cheap_operation(x1)
            out = torch.cat([x1, x2], dim=1)
            return out[:, :self.oup, :, :] * F.interpolate(self.gate_fn(res), size=(out.shape[-2], out.shape[-1]), mode='nearest')


class GhostBottleneckv2(nn.Module):
    """与原文有所出入,在消融实验中每层都添加了DFC,这里前两层还是用的原本v1版本"""
    def __init__(self, in_chs, mid_chs, out_chs, dw_kernel_size=3,
                 stride=1, layer_id=None):
        super(GhostBottleneckv2, self).__init__()
        self.stride = stride

        # Point-wise expansion
        if layer_id <= 1:
            self.ghost1 = GhostModulev2(in_chs, mid_chs, relu=True, mode='original')
        else:
            self.ghost1 = GhostModulev2(in_chs, mid_chs, relu=True, mode='attn')

        # Depth-wise convolution
        if self.stride > 1:
            self.conv_dw = nn.Conv2d(mid_chs, mid_chs, dw_kernel_size, stride=stride,
                                     padding=(dw_kernel_size-1)//2, groups=mid_chs, bias=False)
            self.bn_dw = nn.BatchNorm2d(mid_chs)

        self.ghost2 = GhostModulev2(mid_chs, out_chs, relu=False,mode='original')

        # shortcut
        if (in_chs == out_chs and self.stride == 1):
            self.shortcut = nn.Sequential()
        else:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_chs, in_chs, dw_kernel_size, stride=stride,
                          padding=(dw_kernel_size-1)//2, groups=in_chs, bias=False),
                nn.BatchNorm2d(in_chs),
                nn.Conv2d(in_chs, out_chs, 1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_chs),
            )

    def forward(self, x):
        residual = x
        x = self.ghost1(x)
        if self.stride > 1:
            x = self.conv_dw(x)
            x = self.bn_dw(x)
        x = self.ghost2(x)
        x += self.shortcut(residual)
        return x


class BottleneckBlockWithBAM(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(BottleneckBlockWithBAM, self).__init__()

        # Standard bottleneck block without attention
        self.bottleneck = nn.Sequential(
            nn.Conv2d(in_channels, out_channels // 4, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels // 4),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels // 4, out_channels // 4, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels // 4),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels // 4, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels),
        )

        # BAM module
        self.bam = BAMAttention(out_channels)

        # Identity mapping for the residual connection
        if in_channels != out_channels:
            self.identity_mapping = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False)
        else:
            self.identity_mapping = nn.Identity()

    def forward(self, x):
        identity = self.identity_mapping(x)
        x = self.bottleneck(x)
        x = self.bam(x)
        return x + identity


class SEBasicBlock(nn.Module):
    expansion = 1
    def __init__(self, inplanes, planes, stride=1, downsample=False, reduction=16):
        super(SEBasicBlock, self).__init__()
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes, 1)
        self.bn2 = nn.BatchNorm2d(planes)
        self.se = SEAttention(planes, reduction)
        self.downsample = downsample
        self.stride = stride
        self.conv_down = nn.Sequential(
            conv1x1(inplanes, planes * self.expansion, self.stride),
            nn.BatchNorm2d(planes * self.expansion),
        )

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.se(out)

        if self.downsample:
            residual = self.conv_down(x)

        out += residual
        out = self.relu(out)

        return out


class SEBottleneck(nn.Module):
    expansion = 4
    def __init__(self, inplanes, planes, stride=1, downsample=False, reduction=16):
        super(SEBottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)
        self.se = SEAttention(planes * 4, reduction)
        self.downsample = downsample
        self.stride = stride
        self.conv_down = nn.Sequential(
            conv1x1(inplanes, planes * self.expansion, self.stride),
            nn.BatchNorm2d(planes * self.expansion),
        )

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)
        out = self.se(out)

        if self.downsample:
            residual = self.conv_down(x)

        out += residual
        out = self.relu(out)

        return out