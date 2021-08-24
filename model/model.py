import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np

from base import BaseModel

class MaskModel(nn.Module):
    """
    Basic model format
    """
    def __init__(self, num_classes=18):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 125 * 93, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.flatten(1) # flatten all dimensions except batch  # [B, 16, 125, 93]
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class PretrainModelTV(nn.Module):
    """
    torch vision pretrain model format
    https://pytorch.org/vision/stable/models.html
    """
    def __init__(self, model_name='resnet18',num_classes=18):

        super().__init__()
        self.num_classes = num_classes
        self.model = getattr(torchvision.models, model_name)(pretrained=True)
        print("the number of class labels :", self.model.fc.weight.shape[0])
        self.model.fc = torch.nn.Linear(in_features=512,
                                            out_features=self.num_classes, bias=True)
        
        torch.nn.init.xavier_uniform_(self.model.conv1.weight)
        torch.nn.init.xavier_uniform_(self.model.fc.weight)
        stdv = 1/np.sqrt(self.num_classes)
        self.model.fc.bias.data.uniform_(-stdv, stdv)

    def forward(self, x):
        return self.model(x)