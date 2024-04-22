"""Unit tests for fetching and loading datasets"""

import unittest
import pandas as pd
import numpy as np
import shutil

from synthetic_aia_mia.fetch_data import split
from synthetic_aia_mia.fetch_data import adult
from synthetic_aia_mia.fetch_data import utk


class TestAdult(unittest.TestCase):
    """Test for the adult module of fetch_data package."""
    def test_sensitive(self):
        """Test if sensitive attribute is used according to the sensitive' parameter in adult loader."""
        data = adult.load(sensitive=[])
        data_train = data["train"].load()
        data_test = data["test"].load()
        self.assertFalse("sex" in data_train.columns)
        self.assertFalse("sex" in data_test.columns)
        self.assertFalse("race" in data_train.columns)
        self.assertFalse("race" in data_test.columns)
        del data_train
        del data_test

        data = adult.load(sensitive=["sex"])
        data_train = data["train"].load()
        data_test = data["test"].load()
        self.assertTrue("sex" in data_train.columns)
        self.assertTrue("sex" in data_test.columns)
        self.assertFalse("race" in data_train.columns)
        self.assertFalse("race" in data_test.columns)
        del data_train
        del data_test

        data = adult.load(sensitive=["race"])
        data_train = data["train"].load()
        data_test = data["test"].load()
        self.assertFalse("sex" in data_train.columns)
        self.assertFalse("sex" in data_test.columns)
        self.assertTrue("race" in data_train.columns)
        self.assertTrue("race" in data_test.columns)
        del data_train
        del data_test

        data = adult.load(sensitive=["race","sex"])
        data_train = data["train"].load()
        data_test = data["test"].load()
        self.assertTrue("sex" in data_train.columns)
        self.assertTrue("sex" in data_test.columns)
        self.assertTrue("race" in data_train.columns)
        self.assertTrue("race" in data_test.columns)
        del data_train
        del data_test

        self.assertEqual(len(np.unique(data["train"].load()["PINCP"].to_numpy())),2)
        #Remove the dataset
        shutil.rmtree("data")

class TestUtk(unittest.TestCase):
    """Test for the utk module of fetch_data package."""
    def test_sensitive(self):
        """Test if sensitive attribute is used according to the sensitive' parameter in utk loader."""
        return
        data = utk.load(sensitive=[])
        self.assertFalse("sex"in data["train"].keys())
        self.assertFalse("sex"in data["test"].keys())
        self.assertFalse("race" in data["train"].keys())
        self.assertFalse("race" in data["test"].keys())

        data = utk.load(sensitive=["sex"])
        self.assertTrue("sex"in data["train"].keys())
        self.assertTrue("sex"in data["test"].keys())
        self.assertFalse("race" in data["train"].keys())
        self.assertFalse("race" in data["test"].keys())
        
        data = utk.load(sensitive=["race"])
        self.assertFalse("sex"in data["train"].keys())
        self.assertFalse("sex"in data["test"].keys())
        self.assertTrue("race" in data["train"].keys())
        self.assertTrue("race" in data["test"].keys())

        data = utk.load(sensitive=["sex","race"])
        self.assertTrue("sex"in data["train"].keys())
        self.assertTrue("sex"in data["test"].keys())
        self.assertTrue("race" in data["train"].keys())
        self.assertTrue("race" in data["test"].keys())

        #Remove the dataset
        shutil.rmtree("data_format")
        shutil.rmtree("data_raw")
