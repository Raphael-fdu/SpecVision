import os
import numpy as np
import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval

from random import shuffle
from torch.utils.data import DataLoader
from nets.lenet import Dataset
from scipy.signal import savgol_filter

Xs = np.load("Xs.npy")[::8]

transform = transforms.Compose([transforms.Resize([224, 224]),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.0943, 0.0428, 0.1029], std=[0.4348, 0.3602, 0.1520])])

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def batch_normalization(data):
    return np.array([normalization(row) for row in data])


def load_data(data_path, label_path, img_size, train_ratio, batch_size):
    """
    Process data into dataloaders, and do train/test split.
    """
    # load data and labels from file
    specs = np.load(label_path)

    filenames = np.array(
        [os.path.join(data_path, f"{i + 1}.jpg") for i in range(1000)])

    labels = np.array([normalization(line) for line in specs])

    test_filenames_ = np.loadtxt("test_filenames.txt", delimiter="\n", dtype=str)

    # get train/test filenames
    test_filenames = np.array([os.path.join(data_path, filename)
                              for filename in test_filenames_])

    train_filenames = [i for i in filenames if i not in test_filenames]

    # get train/test indices
    train_indices = []
    for i in train_filenames:
        train_indices.append(np.argwhere(filenames == i).squeeze())
    train_indices = np.array(train_indices)

    test_indices = []
    for i in test_filenames:
        test_indices.append(np.argwhere(filenames == i).squeeze())
    test_indices = np.array(test_indices)

    # wrap train and test data into dataloaders
    transform = transforms.Compose([transforms.Resize([img_size, img_size]),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=[0.0943, 0.0428, 0.1029], std=[0.4348, 0.3602, 0.1520])])


    train_dataset = Dataset(
        filenames[train_indices], labels[train_indices], transform=transform)
    valid_dataset = Dataset(
        filenames[test_indices], labels[test_indices], transform=transform)

    train_loader = DataLoader(
        dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=12)
    valid_loader = DataLoader(
        dataset=valid_dataset, batch_size=batch_size, shuffle=False, num_workers=12)

    return train_loader, valid_loader


def train(model, train_loader, criterion, optimizer, device):
    model.train()
    for _, (X, y) in enumerate(train_loader):
        X, y = X.to(device), y.squeeze().to(device)
        out = model(X)
        loss = criterion(out, y)
        loss.backward()

        optimizer.step()
        optimizer.zero_grad()


def valid(model, valid_loader, criterion, device):
    model.eval()
    losses = []
    for _, (X, y) in enumerate(valid_loader):
        X, y = X.to(device), y.squeeze().to(device)
        out = model(X)
        loss = criterion(out, y).detach().cpu().numpy()
        losses.append(loss)
    losses = np.array(losses)
    val_loss = losses.mean()
    return val_loss


def specGen(model, X):
    out = model(X)
    out = out.cpu().detach().numpy().squeeze()
    plt.plot(Xs, out)
    filename = "test"
    plt.savefig(os.path.join("predicted_specs", str(filename)+".jpg"))
    plt.clf()


def plot_specs():
    Xs = np.load("Xs.npy")[::8]
    Ys = np.load("20210716_spec_128pts.npy")
    for i in range(len(Ys)):
        plt.plot(Xs, Ys[i])
        plt.savefig(os.path.join("label_specs_plots", str(i)+".jpg"))
        plt.clf()


def flattenBaseline_(y):
    return BaselineRemoval(y).ZhangFit()


def smooth_(y):
    return savgol_filter(y, 53, 3)


def normalization_(y):
    range_ = y.max() - y.min()
    return (y-y.min())/range_


def specProc_(y):
    y = flattenBaseline_(y)
    y = smooth_(y)
    out = normalization_(y)
    return out


def getPeakAvgWL(x, y):
    y = specProc_(y)
    halfPeakMask = np.argwhere(y > 0.5)
    peakAvgWL = x[halfPeakMask[0].item() + len(halfPeakMask)//2]
    return peakAvgWL


def getFWHM(x, y):
    y = specProc_(y)
    halfPeakMask = np.argwhere(y > 0.5)
    fwhm = x[halfPeakMask[-1].item()] - x[halfPeakMask[0].item()]
    return fwhm


if __name__ == "__main__":
    plot_specs()
