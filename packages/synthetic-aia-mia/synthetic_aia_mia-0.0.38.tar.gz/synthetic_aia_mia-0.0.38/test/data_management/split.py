
import unittest
import pandas as pd
import numpy as np
import shutil

from synthetic_aia_mia.fetch_data import split
from synthetic_aia_mia.fetch_data import adult

class TestSplit(unittest.TestCase):
    """Test for the split module of fetch_data package."""
    def test_split(self):
        """Test if data is well splet."""
        data = np.random.randint(-10,10,[10,4])
        data = np.hstack([data,np.random.randint(0,2,[10,1])])
        columns = ["cookie","victore","sally","domino","PINCP"]
        df = pd.DataFrame(data=data,columns=columns)
        data_split = split.split_pandas(df)
        self.assertEqual(len(data_split["train"]),8)
        self.assertEqual(len(data_split["test"]),2)
