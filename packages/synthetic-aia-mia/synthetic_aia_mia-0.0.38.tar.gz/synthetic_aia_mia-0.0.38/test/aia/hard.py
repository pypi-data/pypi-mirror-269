"""Unit tests for neural network for attribute inference attack"""

import unittest
import pandas as pd
import numpy as np
import torch

from synthetic_aia_mia.aia import Hard
from synthetic_aia_mia.fetch_data import Dataset

class TestHard(unittest.TestCase):
    """Test for aia"""

    def test_predict_not_trained(self):
        """Test if an exception is raised if predict is called but the model is not trained."""
        df = pd.DataFrame([])
        clf = Hard()
        with self.assertRaises(AssertionError) as cm:
            clf.predict(df)

    def test_predict_trained(self):
        """Test if a trained model in the hyperparameter optimization interface can make a prediction."""
        N = 1000
        y = np.random.randint(0,2,[N,1])
        y = np.hstack([y, np.random.randint(0,5,[N,2])])
        data = np.hstack([y])
        df = pd.DataFrame(data, columns=["hard","sex","race"])
        dset = Dataset()
        dset.update(df)

        clf = Hard()
        clf.fit(dset)
        pred = clf.predict(dset).load()

        self.assertTrue("sex_hard" in pred.columns)
        self.assertTrue("sex" in pred.columns)
        self.assertTrue("race_hard" in pred.columns)
        self.assertTrue("race" in pred.columns)
        self.assertEqual(len(pred),N)
