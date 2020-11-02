import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchvision import datasets, transforms

class Network(nn.Module):
    def __init__(self):
        super().__init__()

        # Input images are 28x28
        self.input_layer = nn.Linear(28*28, 64)        

        # input passes to hidden_1
        self.hidden_1 = nn.Linear(64, 64)

        # hidden_1 passes to hidden_2
        self.hidden_2 = nn.Linear(64, 64)

        # hidden_2 passes to output_layer
        self.output_layer = nn.Linear(64, 10)

    def forward(self, data):
        """
        Defines how data is pushed through the NN.
        """
        # relu = Rectify Linear Unit
        data = F.relu(self.input_layer(data))
        data = F.relu(self.hidden_1(data))
        data = F.relu(self.hidden_2(data))
        data = F.relu(self.output_layer(data))
        
        # Softmax will give us a probability of each choice
        # that sums up to 1.
        return F.log_softmax(data, dim=1)
        

training = datasets.MNIST(
    "./data", train=True, download=True,
    transform=transforms.Compose([transforms.ToTensor()])
)

testing = datasets.MNIST(
    "./data", train=False, download=True,
    transform=transforms.Compose([transforms.ToTensor()])
)

train_set = torch.utils.data.DataLoader(training, batch_size=10, shuffle=True)
test_set = torch.utils.data.DataLoader(testing, batch_size=10, shuffle=True)

network = Network()

# Need to mess around with a learning rate
learn_rate = optim.Adam(network.parameters(), lr=0.01)
epochs = 5


