import unittest
import numpy as np

from synthetic_aia_mia.fetch_data.utk import load
from synthetic_aia_mia.generator.utk import gan


class TestGan(unittest.TestCase)
    dataset = load()["train"].extraction(np.arange(0,10))
    synthetic = gan(dataset,iter_n=1)
    self.assertEqual(len(dataset), len(synthetic))
