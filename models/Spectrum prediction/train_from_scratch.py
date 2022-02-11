from matplotlib.pyplot import get
from scipy.signal.signaltools import wiener
import torch
import numpy as np
import time
import yaml
import os
import sys

from torch import nn
from nets.lenet import LeNet
from utils import *
from datetime import datetime

comment = sys.argv[1]
trial = sys.argv[2]

# -------------------------------------- #
# Read fixed hyperparameters
# from config.yaml
# -------------------------------------- #

config = yaml.load(open('config/config.yaml'), Loader=yaml.FullLoader)
lr = config["lr"]
epochs = config["epochs"]
batch_size = config["batch_size"]
train_ratio = config["train_ratio"]
data_path = config["data_path"]
label_path = config["label_path"]
img_size = config["img_size"]

train_loader, valid_loader = load_data(
    data_path, label_path, img_size, train_ratio, batch_size)


def load_model():
 
    model = LeNet()
    
    return model


def train(model, dataloader, criterion, optimizer, epoch):
    model.train()
    losses = []
    for batch_idx, (X, y) in enumerate(dataloader):
        X, y = X.cuda(), y.cuda().squeeze()
        _, out = model(X)
        loss = criterion(out, y)
        losses.append(loss.cpu().item())

        loss.backward()
        if (batch_idx + 1) % 10 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(X), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data.item()))

        optimizer.step()
        optimizer.zero_grad()

    epoch_loss = np.array(losses, dtype=float).mean()
    print()
    print(f"Train: Average loss: {epoch_loss}\n")

    return epoch_loss


def valid(model, dataloader, criterion):
    model.eval()
    losses = []
    for batch_idx, (X, y) in enumerate(dataloader):
        X, y = X.cuda(), y.cuda().squeeze()
        _, out = model(X)

        loss = criterion(out, y).cpu()
        losses.append(loss.item())
        # specGen(model, X[0].reshape(1, 3, 224, 224))

    epoch_loss = np.array(losses).mean()
    # r2 = r2_score(out.cpu().detach().numpy(), y.cpu().detach().numpy())
    print(f"Test: Average loss: {epoch_loss}\n")
    # print(f"R2 score: {r2}")
    return epoch_loss


if __name__ == "__main__":
    # create CNN models

    log = {}

    since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    lenet = load_model().cuda()

    criterion = nn.MSELoss()

    for model in [lenet]:
        print(
            f"============== Currently training {model.__class__.__name__} ================")
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        train_losses = []
        valid_losses = []
        since = time.time()
        for epoch in range(epochs):
            train_losses.append(
                train(model, train_loader, criterion, optimizer, epoch))
            valid_losses.append(valid(model, valid_loader, criterion))
            if epoch > 100:
                min_loss = np.array(valid_losses).min()
                curr_loss = valid_losses[-1]
                if curr_loss == min_loss:
                    torch.save(model, os.path.join(
                        "saved_models", "Lenet_best_model.pth"))
                    print("LeNet Best model saved!")

        train_losses = np.array(train_losses)
        valid_losses = np.array(valid_losses)

        torch.save(model, os.path.join(
            "saved_models", "Lenet_last_model.pth"))

        print(f"Last train loss: {train_losses[-1]}")
        print(f"Last valid loss: {valid_losses[-1]}")

        ###############################################
        ############# test code #######################
        # evaluate the model on the entire training set
        print("start evaluateing on the whole dataset")

        from test import specGen, getRealSpecs

        def compare(criterion, pred, real):
            pred = torch.tensor(pred)
            real = torch.tensor(real)

            mean_loss = criterion(pred, real).item()
            print("Finished.")
            return mean_loss

        whole_filenames = np.array([f"{i+1}.jpg" for i in range(1000)])
        test_filenames = np.loadtxt(
            "test_filenames.txt", delimiter="\n", dtype=str)
        train_filenames = np.array(
            list(set(whole_filenames) - set(test_filenames)))

        test_indices = np.array([int(i[:-4])-1 for i in test_filenames])
        train_indices = np.array([int(i[:-4])-1 for i in train_filenames])

        test_filenames = [os.path.join(
            "20210630_data", i) for i in test_filenames]
        train_filenames = [os.path.join(
            "20210630_data", i) for i in train_filenames]

        print("Inferring the training set ...")
        pred_train = specGen(model, train_filenames)
        real_train = getRealSpecs(train_indices)

        mean_loss = compare(criterion, pred_train, real_train)
        print(f"Mean loss on the entire training set: {mean_loss}")
        ################## test code ##################
        ###############################################

        log["trial"] = trial
        log["Start time"] = since
        log["End time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log["Last train loss"] = train_losses[-1]
        log["Last valid loss"] = valid_losses[-1]
        log["Epochs"] = epochs
        log["lr"] = lr
        log["comment"] = comment

        with open("log", "a") as f:
            f.write("# ----------------- #\n")
            for key, val in log.items():
                f.write(f"{key}:{val}\n")
            f.flush()
