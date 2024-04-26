"""Unit test for ctgan generator an adult."""

import unittest
import numpy as np
import pandas as pd

from synthetic_aia_mia.fetch_data import Dataset
from synthetic_aia_mia.generator.adult import ctgan

class TestCtgan(unittest.TestCase):
    """Test on ctgan generator."""

    def test_length(self):
        """Test if generator generates as many datapoints as there are in real data."""
        data = np.random.randint(0,2,[10,1])
        data = np.hstack([data,np.random.normal(0,1,[10,1])])
        df = pd.DataFrame(data,columns=["cookie","victore"])
        dadata = Dataset()
        dadata.update(df)
        synthetic_aia_mia = ctgan(dadata).load()

        self.assertEqual(len(df),len(synthetic_aia_mia))
        self.assertEqual(len(df.columns),len(synthetic_aia_mia.columns))
        for i in range(len(df.columns)):
            self.assertEqual(df.columns[i],synthetic_aia_mia.columns[i])


