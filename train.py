import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

bo_words = []
pins = []
yx = []

for intent in intents['intents']:
    pin = intent['tag']
    pins.append(pin)
    for pattern in intent['patterns']:
        f = tokenize(pattern)
        bo_words.extend(f)
        yx.append((f, pin))


ignore_words = ['?', '.', '!']
all_words = [stem(f) for f in bo_words if f not in ignore_words]

bo_words = sorted(set(bo_words))
pins = sorted(set(pins))

print(len(yx), "patterns")
print(len(pins), "tags:", pins)
print(len(bo_words), "unique stemmed words:", bo_words)


A_train = []
Z_train = []
for (pattern_sentence, pin) in yx:
    
    bag = bag_of_words(pattern_sentence, bo_words)
    A_train.append(bag)
    
    label = pins.index(pin)
    Z_train.append(label)

A_train = np.array(A_train)
Z_train = np.array(Z_train)
 
num_epochs = 900
bat_size = 7
learn_rate = 0.001
in_size = len(A_train[0])
hid_size = 8
out_size = len(pins)
print(in_size, out_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(A_train)
        self.a_data = A_train
        self.z_data = Z_train

    
    def __getitem__(self, index):
        return self.a_data[index], self.z_data[index]

    
    def __len__(self):
        return self.n_samples

datas = ChatDataset()
train_loader = DataLoader(dataset=datas,
                          batch_size=bat_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(in_size, hid_size, out_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learn_rate)

for epoch in range(num_epochs):
    for (alpha, labels) in train_loader:
        alpha = alpha.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        outputs = model(alpha)
        loss = criterion(outputs, labels)
        
       
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"in_size": in_size,
"hid_size": hid_size,
"out_size": out_size,
"bo_words": bo_words,
"pins": pins
}

FILE = "Files.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
