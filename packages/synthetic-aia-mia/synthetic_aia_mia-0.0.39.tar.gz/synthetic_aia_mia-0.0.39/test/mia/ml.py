"""Unit tests for neural network for membership inference attack"""

import unittest
import pandas as pd
import numpy as np
import torch

from synthetic_aia_mia.mia import ml
from synthetic_aia_mia.fetch_data import Dataset

class TestAdultNN(unittest.TestCase):
    """Test for mia"""

    def test_predict_not_trained(self):
        """Test if an exception is raised if predict is called but the model is not trained."""
        df = pd.DataFrame([])
        clf = ml.MiaNN()
        with self.assertRaises(AssertionError) as cm:
            clf.predict(df)

    def test_neural_network(self):
        """Test if the pytroch model trains and predicts."""
        N = 100
        x = np.random.uniform(0,1,[N,1])
        x = np.hstack([x,np.random.randint(0,2,[N,1])])
        df = pd.DataFrame(x, columns=["loss" ,"member"])
        config = {"l1":2,"l2":2,"lr":0.001,"batch_size":1}
        clf = ml._train(config,df,stand_alone=True)
        x = torch.tensor(np.random.uniform(0,1,[N,1]),dtype=torch.float)
        y = clf(x)
        self.assertEqual(len(y),N)

    def test_predict_trained(self):
        """Test if a trained model in the hyperparameter optimization interface can make a prediction."""
        N = 1000
        x = np.random.uniform(0,1,[N,1])
        y = np.random.randint(0,2,[N,1])
        data = np.hstack([x,y])
        df = pd.DataFrame(data, columns=["loss","member"])
        dset = Dataset()
        dset.update(df)

        clf = ml.MiaNN()
        clf.fit(dset)
        pred = clf.predict(dset).load()

        self.assertTrue("mia" in pred.columns)
        self.assertTrue("member" in pred.columns)
        self.assertEqual(len(pred),N)
