import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

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
        data = self.output_layer(data)

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

for epoch in range(epochs):
    for data in train_set:
        # image is all of the params of an image in a flattened tensor object
        # output is the "labels" for each image (the labels)
        image, output = data
        network.zero_grad()
        result = network(image.view(-1, 28*28))
        # Using "loss" (error) to help train the network
        loss = F.nll_loss(result, output)
        loss.backward()
        learn_rate.step()
    print(loss)

# Puts the network in eval mode for testing
network.eval()
correct = 0
total = 0

# Turns off learning
with torch.no_grad():
    for data in test_set:
        image, output = data
        results = network(image.view(-1, 28*28))
        for index, tensor_value in enumerate(results):
            total += 1
            if torch.argmax(tensor_value) == output[index]:
                correct += 1

accuracy = correct / total
print("Accuracy:", accuracy)

# Look at image processing. This is the work that pytorch does for us
# when setting up test data.
from PIL import Image
import numpy as np
import PIL.ImageOps

img = Image.open("./6.jpg")
# convert to grayscale
img = img.resize((28, 28))
img.convert("L")

plt.imshow(img)

img = np.array(img)
img = img / 255
image = torch.from_numpy(img)
image = image.float()

result = network.forward(image.view(-1, 28*28))
print(torch.argmax(output))
