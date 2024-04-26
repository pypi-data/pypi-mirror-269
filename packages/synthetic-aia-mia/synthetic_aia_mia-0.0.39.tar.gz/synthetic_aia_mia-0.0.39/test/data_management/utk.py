import unittest 
import numpy as np

from synthetic_aia_mia.fetch_data import utk 

class TestLoadUtk(unittest.TestCase):
    """Test utk loader with memory management."""
    def test_loader(self):
        """Test if data can be accessed."""
        dset = utk.load()["train"]
        self.assertEqual(np.shape(dset[12][0])[0],3)
        self.assertEqual(np.shape(dset[120][0])[1],50)
        self.assertEqual(np.shape(dset[314][0])[2],50)

    def test_extraction(self):
        """Test if a list of index can make a new StorageDataset."""
        dset = utk.load()["train"]
        eDset = dset.extraction([324,3,9])
        self.assertEqual(len(eDset),3)
        self.assertEqual(dset.x[324],eDset.x[0])
        self.assertEqual(dset.x[3],eDset.x[1])
        self.assertEqual(dset.x[9],eDset.x[2])

