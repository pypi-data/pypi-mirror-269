"Tests metrics"
import unittest
import numpy as np
import pandas as pd

from synthetic_aia_mia.metrics import balanced_accuracy
from synthetic_aia_mia.fetch_data import Dataset
 
class TestBalancedAccuracy(unittest.TestCase):
    """Balanced Accuracy testing."""

    def test_balanced_accuracy(self):
        x = np.array([[0,0],
                      [0,0],
                      [0,0],
                      [0,1],
                      [1,1]])
        df = pd.DataFrame(x, columns=("yhat","y"))
        dset = Dataset()
        dset.update(df)
        ba = balanced_accuracy(dset, "y", "yhat")
        self.assertEqual(ba,0.75)
