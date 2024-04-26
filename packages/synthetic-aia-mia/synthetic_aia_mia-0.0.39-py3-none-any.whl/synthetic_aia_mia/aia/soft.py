"""Define structures to manage and interface a fully connected neural network for attribute inference attack using soft labels."""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from functools import partial
import tempfile
import os
import logging

#Pytorch 
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset

#Ray tune
from ray import train, tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.hyperopt import HyperOptSearch
from ray.train import Checkpoint

from ..fetch_data import Dataset

class AiaDataset(Dataset):
    """Pytorch dataset to handle aia with soft labels."""
    def __init__(self, data):
        """Make data conversion for pytorch integration.

        :param data: dataset to convert.
        :type data: pandas.dataframe
        """
        y = data["attribute"].to_numpy()
        self.y = torch.from_numpy(y).type(torch.float)
        self.x = torch.from_numpy(data[["soft0","soft1"]].to_numpy()).type(torch.float)

    def __len__(self):
        """Length of dataset."""
        return len(self.y)

    def __getitem__(self, idx):
        """Fetch ith data point.

        :param idx: Data index.
        :type idx: int or array of int
        """
        return self.x[idx], self.y[idx]

class TabularNN(nn.Module):
    """Pytorch neural network for adult."""
    def __init__(self, input_size, l1, l2, output_size):
        """Sets layers for a neural network.

        :param input_size: Number of features.
        :type input_size: int
        :param hidden_size: Number of neurons/hidden layer.
        :type hidden_size: int
        :param l1: Size of the first layer.
        :type l1: int
        :param l2: Size of the second layer.
        :type l2: int
        :param output_size: Number classes in the labels.
        :type output_size: int
        """

        super(TabularNN, self).__init__()
        self.fc1 = nn.Linear(input_size, l1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """Forward pass in the neural network.

        :param x: Data points.
        :type x: torch.tensor
        :return: Neural network function applied to x.
        :rtype: torch.tensor
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        #x = self.sigmoid(x)
        return x

class AiaNN:
    """Wrapper arround pytorch neural network. Interfare for hyper parameter optimisation using raytune."""
    def __init__(self):
        self.trained = False

    def fit(self, dadata, attrib):
        """Train and tune hyper parameters.
        
        :parameter data: Dataset the will be split for training and hyper parameter tuning. Dataset must contain columns called "soft0" and "soft1" used as features.
        :type dadata: fetch_data.Dataset
        :param attrib: Sensitive attribute to attack. A column of dadata.
        :type attrib: str
        """

        #Soft label preporcessing
        data = dadata.load()[["soft0", "soft1",attrib]]
        x = data[["soft0", "soft1"]].to_numpy()
        self.scaler = StandardScaler()
        self.scaler.fit(x)
        x = self.scaler.transform(x)
        x = pd.DataFrame(x,columns=["soft0", "soft1"])
        data["soft0"] = x["soft0"]
        data["soft1"] = x["soft1"]
        data.rename({attrib:"attribute"},axis=1,inplace=True)
        self.attrib = attrib

        #Sensitive attribute preprocessing
        self.label_encoder = _LabelEncoder()
        y = data["attribute"].to_numpy().astype(int)
        self.label_encoder.fit(y)
        
        ricotta = self.label_encoder.transform(y)
        ricotta = pd.DataFrame(ricotta,columns=["attribute"])
        data["attribute"] = ricotta["attribute"]

        search_space = {
                "l1": tune.choice([2 ** i for i in range(9)]),
                "l2": tune.choice([2 ** i for i in range(9)]),
                "lr": tune.loguniform(1e-4, 1e-1),
                "batch_size": tune.choice([8, 16, 32, 64, 128])
                }

        asha_scheduler = ASHAScheduler(
                time_attr='training_iteration',
                metric='loss',
                mode='min',
                max_t=100,
                grace_period=10,
                reduction_factor=3,
                brackets=1
                )

        hyperopt_search = HyperOptSearch(search_space, metric="loss", mode="min")

        tune_config = tune.TuneConfig(
                num_samples=20,
                scheduler=asha_scheduler,
                search_alg=hyperopt_search
                )

        logging.debug(data)
        tuner = tune.Tuner(
                partial(_train,data=data,stand_alone=False),
                tune_config=tune_config,
                run_config=train.RunConfig(stop=_stop_train)
                )

        results = tuner.fit()

        #Real training on full train dataset (no validation)
        #Using best hyper parameters 
        num_mod = len(np.unique(data["attribute"].to_numpy()))
        best_result = results.get_best_result("loss","min")
        best_trained_model = TabularNN(2,best_result.config["l1"], best_result.config["l2"],num_mod)
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        checkpoint_path = os.path.join(best_result.checkpoint.to_directory(), "checkpoint.pt")

        model_state, optimizer_state = torch.load(checkpoint_path)
        best_trained_model.load_state_dict(model_state)
        
        self.model = best_trained_model
        self.trained=True

    def predict(self, dadata):
        """Use a trained TabularNN to predict label of dataset.

        :param dadata: Dataset to evaluate.
        :type dadata: fetch_data.Dataset
        :return: Input dataset completed with hard labels, soft labels and loss.
        :rtype: fetch_data.Dataset
        """
        if not(self.trained):
            raise AssertionError(f"{self} must be trained prioir to predict")
        with torch.no_grad():
            criterion = nn.CrossEntropyLoss()
            data = dadata.load()
            x = data[["soft0", "soft1"]].to_numpy()
            x = self.scaler.transform(x)
            x = torch.from_numpy(x).float()
            output = self.model(x)

            yhard = np.argmax(output,axis=1)
        yhard = self.label_encoder.inverse_transform(yhard)
        data[self.attrib+"_soft"] = yhard
        dadata.update(data)
        return dadata


def _pandas_to_dataset(data):
    """Split pands dataset into training and validation and convert into pytorch dataset.

    :param data: Dataset that will be split for validation.
    :type data: pandas.dataframe
    :return: Training and validation dataset (train,validation).
    :rtype: tuple of torch.utils.data.dataset
    """
    skf = StratifiedKFold(shuffle=True,random_state=123)

    for train,validation in skf.split(data,data["attribute"]):
        pass
    train_dataset = AiaDataset(data.iloc[train])
    validation_dataset = AiaDataset(data.iloc[validation])
    return train_dataset, validation_dataset

        
def _stop_train(trial_id, result):
    """Tell tray tune to stop training after 20 iterations or when overfitting.

    :param trial_id:
    :type trial_id:
    :param result:
    :type result:
    """
    over_iter = result["training_iteration"] >= 20
    val_loss = result["val_loss"]
    N = len(val_loss)
    if N<5:
        overfit = False
    else:
        overfit = False
        for i in range(1,5):
            overfit = overfit or val_loss[-5]<= val_loss[-i]
        overfit = overfit

    return overfit or over_iter

def _train(config, data, stand_alone=False):
    """Train TabularNN with ray_tune hyper parameter tuning.

    :param data: Dataset that will be split for validation.
    :type data: pandas.dataframe
    :param stand_alone: (Optional default=False) If True _train does not use ray.tune and return the trained model.
    :type return_model: bool
    """
    num_mod = len(np.unique(data["attribute"].to_numpy()))
    net = TabularNN(2,config["l1"],config["l2"],num_mod)

    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda:0"
    net.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=config["lr"])

    train_dataset, validation_dataset = _pandas_to_dataset(data)

    torch.manual_seed(1234)
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
    )
    torch.manual_seed(1234)
    validation_loader = torch.utils.data.DataLoader(
    validation_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
)

    val_loss_hist = []

    for epoch in range(0, 100):  # loop over the dataset multiple times
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

class _LabelEncoder:
    """Create label in [0,C-1]."""

    def __init__(self):
        pass
    def fit(self, x):
        """Create label space.

        :param x:Array of labels
        :type x: array like
        """
        self.space = np.unique(x)

    def transform(self, x):
        """Uses fitted space to get normalized labels.
        This is a preprocessing step.

        :param x: Labels.
        :type x: numpy.ndarray
        :return: Normalized labels.
        :rtype: numpy.ndarray
        """
        with open("log", "w") as f:
            f.write(str(x))
        return np.searchsorted(self.space, x)

    def inverse_transform(self,x): 
        """From normalized labels return actual values. 
        This is a post processing step.

        :param x: Normalized labels.
        :type x: numpy.ndarray
        :return: Post processed labels.
        :rtype: numpy.ndarray
        """
        return self.space[x]

