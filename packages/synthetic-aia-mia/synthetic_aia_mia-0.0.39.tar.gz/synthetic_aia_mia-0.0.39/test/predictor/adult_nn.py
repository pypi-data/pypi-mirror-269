"""Unit tests for adult neural network"""

import unittest
import pandas as pd
import numpy as np
import torch
import logging
logging.basicConfig(filename='adult.log', encoding='utf-8', level=logging.INFO)

from synthetic_aia_mia.predictor import adult
from synthetic_aia_mia.fetch_data import Dataset

class TestAdultNN(unittest.TestCase):
    """Test for the adult module of predictor package."""

    def test_predict_not_trained(self):
        """Test if an exception is raised if predict is called but the model is not trained."""
        df = pd.DataFrame([])
        clf = adult.AdultNN()
        with self.assertRaises(AssertionError) as cm:
            clf.predict(df)

    def test_neural_network(self):
        """Test if the pytroch model trains and predicts."""
        x = np.random.randint(0,2,[100,2])
        df = pd.DataFrame(x, columns=["x","PINCP"])
        config = {"l1":2,"l2":2,"l3":2,"l4":2,"lr":0.001,"batch_size":1}
        clf = adult._train(config,df,stand_alone=True)
        x = torch.tensor([[1],[2],[3],[4],[5]],dtype=torch.float)
        y = clf(x)
        self.assertEqual(len(y),5)

    def test_predict_trained(self):
        """Test if a trained model in the hyperparameter optimization interface can make a prediction."""
        N = 100
        x = np.random.uniform(0,1,[N,1])
        y = np.random.randint(0,2,[N,1])
        data = np.hstack([x,y])
        df = pd.DataFrame(data, columns=["x","PINCP"])
        dataset = Dataset()
        dataset.update(df)

        clf = adult.AdultNN()
        clf.fit(dataset)
        pred = clf.predict(dataset).load()

        self.assertTrue("soft0" in pred.columns)
        self.assertTrue("soft1" in pred.columns)
        self.assertTrue("hard" in pred.columns)
        self.assertTrue("loss" in pred.columns)
        self.assertEqual(len(pred["PINCP"]),N)
