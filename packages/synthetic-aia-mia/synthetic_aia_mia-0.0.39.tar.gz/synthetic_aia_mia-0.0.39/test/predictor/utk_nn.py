"""Unit tests for adult neural network"""

import unittest
import pandas as pd
import numpy as np
import torch

from synthetic_aia_mia.predictor import utk
from synthetic_aia_mia.fetch_data.utk import load

class TestUtkNN(unittest.TestCase):
    """Test for the adult module of predictor package."""

    def test_predict_not_trained(self):
        """Test if an exception is raised if predict is called but the model is not trained."""
        df = pd.DataFrame([])
        clf = utk.UtkNN()
        with self.assertRaises(AssertionError) as cm:
            clf.predict(df)

    def test_neural_network(self):
        """Test if the pytroch model trains and predicts."""

        data = load()["train"].extraction([32,9,53,123,4,1,2,23,5])
        config = {"c1":2,"c2":2,"l":10,"lr":0.001,"batch_size":1}
        clf = utk._train(config,data,stand_alone=True,epochs=1)
        x = np.zeros([len(data),3,50,50]).astype(float)
        for i in range(len(data)):
            x[i] = data[i][0]
        x = torch.from_numpy(x).float()
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda:0"
        with torch.no_grad():
            x = x.to(device)
            y = clf(x)
        self.assertEqual(len(y),len(data))

    def test_predict_trained(self):
        """Test if a trained model in the hyperparameter optimization interface can make a prediction."""
        data = load()["train"].extraction([32,9,53,123,4,1,2,23,5])
        clf = utk.UtkNN(epochs=1)
        clf.fit(data)
        pred = clf.predict(data)

        self.assertEqual(len(pred.hard),len(data))
