import sys
import unittest
import pandas as pd
import numpy as np
import shutil
import pickle

from synthetic_aia_mia.fetch_data import Dataset
class TestDataset(unittest.TestCase):
    """Test for the fetch_data.dataset"""
    def test_integrity(self):
        """Test if data preserved."""
        def _a(data):
            """Turn some data into fetch_data.Datatset.

            :param data: Data to be embeded.
            :type data: anything that can be pickled
            """
            dataset = Dataset()
            dataset.update(data)
            return dataset

        data = np.random.randint(-10,10,[10,4])
        data = np.hstack([data,np.random.randint(0,2,[10,1])])
        columns = ["cookie","victore","sally","domino","PINCP"]
        df = pd.DataFrame(data=data,columns=columns)
        dataset = _a(df)
        loaded = dataset.load()
        for i in range(10):
            for j in range(5):
                self.assertEqual(df.iloc[i][j],loaded.iloc[i][j])

    def test_size(self):
        """Tets if fetch_data.dataset can be manipulated without filled up memroy."""
        data = np.zeros([1000,10000]).astype(float)
        print(sys.getsizeof(data))
        dataset = Dataset()
        dataset.update(data)
        print(sys.getsizeof(dataset))

    def test_save(self):
        data = np.array([[0,1],[2,3]])
        df = pd.DataFrame(data, columns=("a", "b"))
        dataset = Dataset()
        dataset.update(df)
        dataset.save("/tmp/data.pickle")
        del dataset
        with open("/tmp/data.pickle",'rb') as f:
            new_df = pickle.load(f)

        for i in range(len(df)):
            for j in range(len(df[i]))
                self.assertEqual(new_df[i][j], df[i][j])

        for col in range(len(list(df.columns))):
            self.assertEqual(list(df.columns)[i], list(new_df.columns)[i])

