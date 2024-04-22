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

class AiaRF:
    """Wrapper arround sklearn random forest"""
    def __init__(self):
        self.trained = False

    def fit(self, dadata, attrib):
        """Train a random forest.
        
        :parameter data: Dataset the will be used for training. Dataset must contain columns called "loss" used as features and "member" used as labels.
        :type dadata: fetch_data.Dataset
        """

        data = dadata.load()[["soft0", "soft1",attrib]]
        x = data[["soft0", "soft1"]].to_numpy()

        self.model = RandomForestClassifier()
        self.model.fit(x,data[attrib].to_numpy())

        self.trained = True

        self.attrib = attrib
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
        yhard = self.model.predict(data[["soft0", "soft1"]].to_numpy())
        data[f"{self.attrib}_soft"] = yhard
        dadata.update(data)
        return dadata


        

