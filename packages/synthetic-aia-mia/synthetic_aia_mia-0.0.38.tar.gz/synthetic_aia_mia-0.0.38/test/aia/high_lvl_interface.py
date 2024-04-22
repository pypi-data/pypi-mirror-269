"""Test the integration in the high level interface class used in experiments."""

import unittest
import numpy as np
import pandas as pd

from synthetic_aia_mia.aia import Aia
from synthetic_aia_mia.fetch_data import Dataset


class TestAia(unittest.TestCase):
    """Test Aia class : high lvl interface for attribute inference attacks."""

    def test_full_stack(self):
        """Test if the attribute inference attack complete the dataset with prediction."""
        N = 100
        x = np.random.uniform(0,1,[N,2])
        x = np.hstack([x,np.random.randint(0,2,[N,4])])
        df = pd.DataFrame(x,columns=["soft0","soft1","hard","PINCP","sex","race"])
        dset = Dataset()
        dset.update(df)

        aia = Aia()
        aia.fit(dset)
        pred = aia.predict(dset).load()

        self.assertTrue("sex_hard" in pred.columns)
        self.assertTrue("sex_soft" in pred.columns)
        self.assertTrue("race_hard" in pred.columns)
        self.assertTrue("race_hard" in pred.columns)

