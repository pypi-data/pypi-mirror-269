"""MIA using a random forest."""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from functools import partial
import tempfile
import os

from ..fetch_data import Dataset

class MiaRF:
    """Wrapper arround sklearn random forest"""
    def __init__(self):
        self.trained = False

    def fit(self, dadata):
        """Train a random forest.
        
        :parameter data: Dataset the will be used for training. Dataset must contain columns called "loss" used as features and "member" used as labels.
        :type dadata: fetch_data.Dataset
        """

        data = dadata.load()[["loss","member"]]
        x = data["loss"].to_numpy().reshape(-1,1)
        self.scaler = StandardScaler()
        self.scaler.fit(x)
        x = self.scaler.transform(x)
        x = pd.DataFrame(x,columns=["loss"])
        data.replace(x,inplace=True)

        self.model = RandomForestClassifier()
        self.model.fit(data["loss"].to_numpy().reshape(-1,1),data["member"].to_numpy())

        self.trained = True


    def predict(self, dadata):
        """Use a trained TabularNN to predict label of dataset.

        :param dadata: Dataset to evaluate.
        :type dadata: fetch_data.Dataset
        :return: Input dataset completed with mia result as a column called "mia".
        :rtype: fetch_data.Dataset
        """
        if not(self.trained):
            raise AssertionError(f"{self} must be trained prioir to predict")

        data = dadata.load()
        yhard = self.model.predict(data["loss"].to_numpy().reshape(-1,1))
        data["mia"] = yhard
        dadata.update(data)
        return dadata


        

