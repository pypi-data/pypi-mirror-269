"""Define structures to manage and interface a CNN for mia on synthetic utk."""

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
import pandas as pd
from functools import partial
import tempfile
import os
import logging

#Pytorch 
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset
import torchvision.transforms as transforms

#Ray tune
from ray import train, tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.hyperopt import HyperOptSearch
from ray.train import Checkpoint

from ..fetch_data import Dataset
from ..fetch_data.split import split_numpy

class UtkDataset(Dataset):
    """Pytorch dataset to handle StorageDataset."""
    def __init__(self, data):
        """Make data conversion for pytorch integration.

        :param data: dataset to convert.
        :type data: fetch_data.utk.StorageDataset
        """
        self.data = data

    def __len__(self):
        """Length of dataset."""
        return len(self.data)

    def __getitem__(self, idx):
        """Fetch ith data point.

        :param idx: Data index.
        :type idx: int or array of int
        """
        x = torch.from_numpy(self.data[idx][0]).float()
        y = torch.from_numpy(np.array(self.data.member[idx])).float()
        return x,y

class CNN(nn.Module):
    """Convolutional neural network for 50x50x3 images.

    :param c1: Output number of channels of the first convolution layer.
    :type c1: int
    :param c2: Output number of channels of the second convolution layer.
    :type c2: int
    :param: Linear size.
    :type l: int
    """
    def __init__(self,c1,c2,l):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, c1, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(c1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(c1, c2, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(c2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.l1 = nn.Linear(12 * 12 * c2, l) # 50x50 image size after two maxpool layers
        self.l2 = nn.Linear(l, 2) # 50x50 image size after two maxpool layers

    def forward(self, x):
        """Forward pass of the cnn.

        :param x: Input batch.
        :type x: torch.tenort
        """
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.l1(out)
        out = self.l2(out)

        return out

class UtkNN:
    """Wrapper arround pytorch neural network. Interfare for hyper parameter optimisation using raytune.

    :param epochs: Number of epochs.
    :type epochs: int"""
    def __init__(self,epochs=500):
        self.trained = False
        self.epochs=epochs

    def fit(self, data):
        """Train and tune hyper parameters.
        
        :parameter data: Dataset the will be split for training and hyper parameter tuning. Dataset must contain a column called "PINCP" used as training label.
        :type dadata: fetch_data.utk.StorageDataset
        """

        search_space = {
                "c1": tune.choice([5,10,20,30,40]),
                "c2": tune.choice([5,10,20,30,40]),
                "l": tune.choice([2 ** i for i in range(9)]),
                "lr": tune.loguniform(1e-5, 1e-1),
                "batch_size": tune.choice([16, 32, 64, 128])
                }

        if self.epochs <10:
            gp = 1
        else:
            gp = 10
        asha_scheduler = ASHAScheduler(
                time_attr='training_iteration',
                metric='loss',
                mode='min',
                max_t=self.epochs,
                grace_period=gp,
                reduction_factor=3,
                brackets=1
                )

        hyperopt_search = HyperOptSearch(search_space, metric="loss", mode="min")

        tune_config = tune.TuneConfig(
                num_samples=20,
                scheduler=asha_scheduler,
                search_alg=hyperopt_search
                )

        tuner = tune.Tuner(
                partial(_train,data=data,stand_alone=False,epochs=self.epochs),
                tune_config=tune_config,
                run_config=train.RunConfig(stop=_stop_train)
                )

        results = tuner.fit()

        #Real training on full train dataset (no validation)
        #Using best hyper parameters 
        best_result = results.get_best_result("loss","min")
        best_trained_model = CNN(best_result.config["c1"], 
                                 best_result.config["c2"],
                                 best_result.config["l"])

        checkpoint_path = os.path.join(best_result.checkpoint.to_directory(), "checkpoint.pt")

        model_state, optimizer_state = torch.load(checkpoint_path)
        best_trained_model.load_state_dict(model_state)
        
        self.model = best_trained_model
        self.trained=True

    def predict(self, data):
        """Use a trained CNN to predict label of dataset.

        :param dadata: Dataset to evaluate.
        :type dadata: fetch_data.utk.StorageDataset
        :return: Input dataset completed with hard labels, soft labels and loss.
        :rtype: fetch_data.Dataset
        """
        if not(self.trained):
            raise AssertionError(f"{self} must be trained prioir to predict")
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda:0"

        self.model.to(device)
        dataset = UtkDataset(data)
        loader = torch.utils.data.DataLoader(
        dataset, batch_size=len(data), shuffle=False, num_workers=8
    )
        with torch.no_grad():
            for x,y in loader:
                x,y = x.to(device),y.to(device)
                criterion = nn.CrossEntropyLoss(reduction='none')
                output = self.model(x)
                ysoft = output.numpy()

                yhard = np.argmax(ysoft,axis=1)

                data.mia_synthetic = yhard

        return data

def _dictionary_to_dataset(data):
    """Split dictionary dataset into train and validation.

    :param data: Dataset that will be split for validation.
    :type data: fetch_data.Dataset    
    :return: Training and validation dataset (train,validation).
    :rtype: tuple of torch.utils.data.dataset
    """
    skf = StratifiedKFold(shuffle=True,random_state=123)
    for train,validation in skf.split(data.y,data.y):
        pass
    train_dataset = UtkDataset(data.extraction(train))
    validation_dataset = UtkDataset(data.extraction(validation))
    return train_dataset, validation_dataset

        
def _stop_train(trial_id, result):
    """Tell tray tune to stop training when overfitting.

    :param trial_id:
    :type trial_id:
    :param result:
    :type result:
    """
    val_loss = result["val_loss"]
    N = len(val_loss)
    if N<5:
        overfit = False
    else:
        overfit = False
        for i in range(1,5):
            overfit = overfit or val_loss[-5]<= val_loss[-i]
        overfit = overfit

    return overfit

def _train(config, data, stand_alone=False,epochs=500):
    """Train CNN with ray_tune hyper parameter tuning.

    :param data: Dataset that will be split for validation.
    :type data: fetch_data.utk.StorageDataset
    :param stand_alone: (Optional default=False) If True _train does not use ray.tune and return the trained model.
    :type return_model: bool
    """
    net = CNN(config["c1"],
                    config["c2"],
                    config["l"])

    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda:0"
    net.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=config["lr"])

    train_dataset, validation_dataset = _dictionary_to_dataset(data)

    torch.manual_seed(1234)
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
    )
    torch.manual_seed(1234)
    validation_loader = torch.utils.data.DataLoader(
    validation_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
)

    val_loss_hist = []

    for epoch in range(0, epochs):  # loop over the dataset multiple times
        running_loss = 0.0
        epoch_steps = 0
        for i, batch_data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = batch_data
            inputs, labels = inputs.to(device), labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels.long())
            loss.backward()
            optimizer.step()

        # Validation loss
        val_loss = 0.0
        val_steps = 0
        total = 0
        correct = 0
        for i, data in enumerate(validation_loader, 0):
            with torch.no_grad():
                inputs, labels = data
                inputs, labels = inputs.to(device), labels.to(device)

                outputs = net(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                loss = criterion(outputs, labels.long())
                val_loss += loss.cpu().numpy()
                val_steps += 1

        val_loss_hist += [val_loss/val_steps]
        #Report back to Raytune
        if not(stand_alone):

           # Here we save a checkpoint. It is automatically registered with
            # Ray Tune and will potentially be accessed through in ``get_checkpoint()``
            # in future iterations.
            # Note to save a file like checkpoint, you still need to put it under a directory
            # to construct a checkpoint.
            with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
                path = os.path.join(temp_checkpoint_dir, "checkpoint.pt")
                torch.save(
                    (net.state_dict(), optimizer.state_dict()), path
                )
                checkpoint = Checkpoint.from_directory(temp_checkpoint_dir)
                train.report({"loss":val_loss/val_steps,
                              "training_iteration":epoch,
                              "val_loss":val_loss_hist},
                             checkpoint=checkpoint,
                             )
    if stand_alone:
        return net
