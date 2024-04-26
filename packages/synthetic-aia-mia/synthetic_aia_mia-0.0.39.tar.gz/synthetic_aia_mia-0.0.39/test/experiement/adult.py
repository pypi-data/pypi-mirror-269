"""Test module for the experiment stack for adult."""
import numpy as np
import pandas as pd
import unittest

from synthetic_aia_mia.experiments import adult
from synthetic_aia_mia.fetch_data import Dataset

class TestAia(unittest.TestCase):
    """Test _aia wrapper."""

    def test_metrics(self):
        """Test if _aia outputs the right metrics."""
        N = 100
        x = np.random.uniform(0,1,[N,2])
        x = np.hstack([x,np.random.randint(0,2,[N,4])])
        df = pd.DataFrame(x,columns=["soft0","soft1","hard","PINCP","sex","race"])
        dset = Dataset()
        dset.update(df)
        metrics = adult._aia(dset)

        for lab in ["hard","soft"]:
            for attrib in ["sex","race"]:
                self.assertTrue(attrib in metrics.keys())
                self.assertTrue(lab in metrics[attrib].keys())
                self.assertTrue("balanced_accuracy" in metrics[attrib][lab].keys())

class TestMia(unittest.TestCase):
    """Test _mia wrapper."""

    def test_metric(self):
        """Test if _mia outputs the right metrics."""
        N = 100
        x = np.random.uniform(0,1,[N,1])
        x = np.hstack([x,np.random.randint(0,2,[N,1])])
        df = pd.DataFrame(x,columns=["loss","member"])
        dset = Dataset()
        dset.update(df)
        metrics = adult._mia(dset)
        self.assertTrue("balanced_accuracy" in metrics.keys())



