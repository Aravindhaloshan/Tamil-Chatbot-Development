import torch
import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self, in_size, hid_size, num_class):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(in_size, hid_size) 
        self.l2 = nn.Linear(hid_size, hid_size) 
        self.l3 = nn.Linear(hid_size, num_class)
        self.relu = nn.ReLU()
    
    def forward(self, a):
        out = self.l1(a)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out
