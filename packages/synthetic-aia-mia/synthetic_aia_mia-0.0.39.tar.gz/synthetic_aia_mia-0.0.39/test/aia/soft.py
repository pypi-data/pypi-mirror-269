"""Unit tests for neural network for attribute inference attack"""

import unittest
import pandas as pd
import numpy as np
import torch
import logging

from synthetic_aia_mia.aia import soft
from synthetic_aia_mia.fetch_data import Dataset

class TestAdultNN(unittest.TestCase):
    """Test for aia"""

    def test_predict_not_trained(self):
        """Test if an exception is raised if predict is called but the model is not trained."""
        df = pd.DataFrame([])
        clf = soft.AiaNN()
        with self.assertRaises(AssertionError) as cm:
            clf.predict(df)

    def test_neural_network(self):
        """Test if the pytroch model trains and predicts."""
        N = 100
        x = np.random.uniform(0,1,[N,2])
        x = np.hstack([x,np.random.randint(0,5,[N,1])])
        df = pd.DataFrame(x, columns=["soft0", "soft1" ,"attribute"])
        config = {"l1":2,"l2":2,"lr":0.001,"batch_size":1}
        clf = soft._train(config,df,stand_alone=True)
        x = torch.tensor(np.random.uniform(0,1,[N,2]),dtype=torch.float)
        y = clf(x)
        self.assertEqual(len(y),N)

    def test_predict_trained(self):
        """Test if a trained model in the hyperparameter optimization interface can make a prediction."""
        N = 100
        x = np.random.uniform(0,1,[N,2])
        y = np.random.randint(2,9,[N,1])
        data = np.hstack([x,y])
        df = pd.DataFrame(data, columns=["soft0", "soft1","sex"])
        dset = Dataset()
        dset.update(df)

        clf = soft.AiaNN()
        clf.fit(dset,"sex")
        pred = clf.predict(dset).load()

        self.assertTrue("sex_soft" in pred.columns)
        self.assertTrue("sex" in pred.columns)
        self.assertEqual(len(pred),N)

class TestAccuracy(unittest.TestCase):
    """Test if the accuracy is correct."""
    def test_predict_trained(self):
        N = 100
        pet = 5
        expected_accuracy = 1 - pet/N
        x = np.random.uniform(0,1,[N,5])
        y = (0.5*(x[:,0] + x[:,1])>0.5)
        perturbation = np.random.randint(0,N,pet)
        y[perturbation][y[perturbation]>0.5] = y[perturbation][y[perturbation]>0.5] - 0.5
        y[perturbation][y[perturbation]<=0.5] = y[perturbation][y[perturbation]<=0.5] + 0.5
        data = np.hstack([x,y])
        df = pd.DataFrame(data, columns=["soft0", "soft1","sex"])
        dset = Dataset()
        dset.update(df)

        clf = soft.AiaNN()
        clf.fit(dset,"sex")
        pred = clf.predict(dset).load()["sex_soft"].to_numpy()
        
        accuracy = np.mean(pred==y)
        self.assertTrue(accuracy > expected_accuracy-0.1)
        self.assertTrue(accuracy < expected_accuracy+0.1)
