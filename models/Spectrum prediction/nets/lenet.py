import torch

from torch import nn
from torch.utils import data
from PIL import Image


class Dataset(data.Dataset):
    "Characterizes a dataset for PyTorch"

    def __init__(self, filenames, labels, transform=None):
        "Initialization"
        self.filenames = filenames
        self.labels = labels
        self.transform = transform

    def __len__(self):
        "Denotes the total number of samples"
        return len(self.filenames)

    def __getitem__(self, index):
        "Generates one sample of data"
        # Select sample
        filename = self.filenames[index]
        X = Image.open(filename)

        if self.transform:
            X = self.transform(X)     # transform

        y = torch.FloatTensor([self.labels[index]])
        return X, y


class LeNet(nn.Module):
    def __init__(self, c=128, l1=512, l2=256):
        super().__init__()
        self.cnn = nn.Sequential(
            # output dim (6 x 27 x 27)
            nn.Conv2d(3, 6, 11, 4, 0),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # output dim (16 x 11 x 11)
            nn.Conv2d(6, 16, 5, 1, 0),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # output dim (120 x 7 x 7)
            # nn.Conv2d(16, c, 5, 1, 0),
            # nn.ReLU()
        )

        self.fcc1 = nn.Sequential(
            nn.Linear(11 * 11 * 16, 512),
            nn.ReLU(),
        )

        self.fcc2 = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
        )


    def forward(self, x):
        x = self.cnn(x).view(x.size()[0], -1)
        latent = self.fcc1(x)
        out = self.fcc2(latent)
        return latent, out
