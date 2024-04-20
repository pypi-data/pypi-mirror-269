import torch
import sys
from pyzjr.Models.backbone import *

def get_clsnetwork(name, num_classes, weights=''):
    if name == 'lenet':
        net = LeNet(num_classes=10)
    elif name == 'alexnet':
        net = AlexNet(num_classes=num_classes)
    elif name == 'vgg16':
        net = vgg16_bn(num_classes=num_classes)
    elif name == 'vgg19':
        net = vgg19_bn(num_classes=num_classes)
    elif name == 'googlenet':
        net = GoogLeNet(num_classes=num_classes)
    elif name == 'resnet18':
        net = resnet18(num_classes=num_classes)
    elif name == 'resnet34':
        net = resnet34(num_classes=num_classes)
    elif name == 'resnet50':
        net = resnet50(num_classes=num_classes)
    elif name == 'resnet101':
        net = resnet101(num_classes=num_classes)
    elif name == 'resnet152':
        net = resnet152(num_classes=num_classes)
    elif name == 'conv2former_n':
        net = Conv2Former_n(num_classes=num_classes)
    elif name == 'conv2former_t':
        net = Conv2Former_t(num_classes=num_classes)
    elif name == 'conv2former_s':
        net = Conv2Former_s(num_classes=num_classes)
    elif name == 'conv2former_l':
        net = Conv2Former_l(num_classes=num_classes)
    elif name == 'conv2former_b':
        net = Conv2Former_b(num_classes=num_classes)
    elif name == 'se_resnet18':
        net = resnet18(num_classes=num_classes, use_se=True)
    elif name == 'se_resnet34':
        net = resnet34(num_classes=num_classes, use_se=True)
    elif name == 'se_resnet50':
        net = resnet50(num_classes=num_classes, use_se=True)
    elif name == 'se_resnet101':
        net = resnet101(num_classes=num_classes, use_se=True)
    elif name == 'se_resnet152':
        net = resnet152(num_classes=num_classes, use_se=True)
    else:
        print('the network name you have entered is not supported yet')
        sys.exit()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    net.to(device)

    if weights != '':
        print('Load weights {}.'.format(weights))
        model_dict = net.state_dict()
        pretrained_dict = torch.load(weights, map_location=device)

        matched_keys = set(model_dict.keys()) & set(pretrained_dict.keys())
        mismatched_keys = set(model_dict.keys()) - set(pretrained_dict.keys())

        for key in matched_keys:
            if model_dict[key].shape == pretrained_dict[key].shape:
                model_dict[key] = pretrained_dict[key]
            else:
                mismatched_keys.add(key)

        if mismatched_keys:
            print("The following keys have mismatched shapes or are not present in the model:")
            for key in mismatched_keys:
                print(f"- {key}")
        else:
            print("All weights were successfully loaded.")
            net.load_state_dict(model_dict)
    else:
        print("\033[31mNo weights specified.Training from scratch.But it does not affect the progress of infering")

    return net