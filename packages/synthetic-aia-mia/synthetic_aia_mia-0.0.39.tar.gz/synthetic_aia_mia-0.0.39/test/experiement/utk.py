"""Test module for the experiment stack for adult."""
import numpy as np
import pandas as pd
import unittest

from synthetic_aia_mia.experiments import utk
from synthetic_aia_mia.fetch_data.utk import load

class TestAia(unittest.TestCase):
    """Test _aia wrapper."""

    def test_metrics(self):
        """Test if _aia outputs the right metrics."""
        N = 100
        data = load()["train"].extraction(np.random.randint(0,200,N))
        data.soft0 = np.random.uniform(0,1,N)
        data.soft1 = np.random.uniform(0,1,N)
        data.hard = np.random.randint(0,2,N)

        metrics = utk._aia(data)

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
        data = load()["train"].extraction(np.random.randint(0,200,N))
        data.loss = np.random.uniform(0,1,N)
        data.member = np.random.randint(0,2,N)
        metrics = utk._mia(data)
        self.assertTrue("balanced_accuracy" in metrics.keys())



