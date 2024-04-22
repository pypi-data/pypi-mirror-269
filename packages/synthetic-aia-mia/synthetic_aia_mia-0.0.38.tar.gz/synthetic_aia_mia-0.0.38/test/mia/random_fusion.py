import unittest
import pandas as pd
import numpy as np

from synthetic_aia_mia.mia import random_fusion
from synthetic_aia_mia.fetch_data import Dataset

class TestFusion(unittest.TestCase):
    """Test if fusion of train and test dataset works."""
    def test_fusion(self):
        train = Dataset()
        train.update(pd.DataFrame([1,1,1,1]))
        test = Dataset()
        test.update(pd.DataFrame([0,0,0]))
        fusion = random_fusion(train,test)
        ful = fusion.load()
        fun = ful.to_numpy()
        self.assertEqual(len(ful),6)
