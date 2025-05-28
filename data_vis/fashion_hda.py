import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image

# Select device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def make_prediction():
    # Get the model path (make sure this is running inside a Houdini Python context)
    import hou
    model_path = hou.pwd().parm('model').eval()

    # Load and prepare model
    model = Net().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))  # map_location to ensure compatibility
    model.eval()  # Call it as a method with ()

    image_path = hou.pwd().parm('image').eval()

    image = Image.open(image_path).convert("L")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28, 28))
    ])

    image = transform(image).to(device)
    with torch.inference_mode():
        output = model(image)
        prediction = torch.argmax(output).item()

    print(f"Prediction: {prediction}")

