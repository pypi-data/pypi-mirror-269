"""Unit tests for adult neural network"""

import unittest
import pandas as pd
import numpy as np
import torch

from synthetic_aia_mia.predictor import adult

class TestAdultNN(unittest.TestCase):
    """Test for the adult module of predictor package."""

    def test_all_the_same(self):
        """Test stop if all the same."""
        val_loss = [1,1,1,1,1]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

    def test_less_than_5(self):
        """Test no stop if < 5."""
        val_loss = [1,1,1,1]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertFalse(stop)

    def test_one_bigger(self):
        """Test stop one is bigger."""
        val_loss = [2,1,3,1,1]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

        val_loss = [2,1,1,1,3]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

        val_loss = [2,1,1,1,3]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

        val_loss = [2,3,1,1,1]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

        val_loss = [2,3,1,3,1]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)
        
        val_loss = [2,3,3,3,3]
        result = {"training_iteration":10,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)

    def test_more_than_20_iter(self):
        """Test stop if more than 20 iterations."""
        val_loss = []
        result = {"training_iteration":20,"val_loss":val_loss}
        stop = adult._stop_train(0,result)
        self.assertTrue(stop)


