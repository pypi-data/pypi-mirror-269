import unittest
import pandas as pd
import numpy as np

from synthetic_aia_mia.mia import random_fusion_storage
from synthetic_aia_mia.fetch_data.utk import load

class TestFusion(unittest.TestCase):
    """Test if fusion of train and test dataset works."""
    def test_fusion(self):
        train = load()["train"].extraction([1,2,3,4])
        test = load()["test"].extraction([1,2])
        fusion = random_fusion_storage(train,test)
        self.assertEqual(len(fusion),4)
        num_of_member = np.sum(fusion.member)
        self.assertEqual(num_of_member,2)
