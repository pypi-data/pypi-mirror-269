"""Test the label encoder class."""

import unittest
import numpy as np

from synthetic_aia_mia.aia import soft

class TestLabelEncoder(unittest.TestCase):
    """Test label encoder is a bijection."""

    def test_transform(self):
        """Test if label encoder.transform is an application.
        ie. each label maps to a unique transformed label."""
        n_clas = 30
        N = 1000
        clas = np.random.randint(123,87456,n_clas)
        x = np.random.choice(clas,N)
        label_encoder = soft._LabelEncoder()
        label_encoder.fit(x)
        y = label_encoder.transform(x)
        dct = {}
        for i,xx in enumerate(x):
            if xx in dct.keys():
                self.assertEqual(dct[xx],y[i])
            else:
                dct[xx] = y[i]

    def test_label_encoder_bijective(self):
        """Test if label encoder is one-to-one."""
        n_clas = 30
        N = 100
        clas = np.random.randint(123,87456,n_clas)
        x = np.random.choice(clas,N)
        label_encoder = soft._LabelEncoder()
        label_encoder.fit(x)
        y = label_encoder.transform(x)
        y = label_encoder.inverse_transform(y)
        
        for i,xx in enumerate(x):
            self.assertEqual(xx,y[i])

    def test_porperly_encoded(self):
        """Test if there is no gap, starts at 0 ends at n_clas-1, same number of classes."""
        #n_clas = 30
        N = 10000
        #clas = np.random.randint(2,9,n_clas)
        #x = np.random.choice(clas,N)
        x = np.random.randint(2,9,[N,1])
        true_clas = len(np.unique(x))

        label_encoder = soft._LabelEncoder()
        label_encoder.fit(x)
        y = label_encoder.transform(x)

        u = np.unique(y)
        self.assertEqual(len(u),true_clas)

        for i in range(len(u)):
            self.assertEqual(u[i],i)
