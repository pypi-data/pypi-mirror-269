"""Membership inference attack."""

import pandas as pd
import numpy as np

from ..fetch_data import Dataset
from .rf import MiaRF
from ..predictor.adult import _pandas_to_dataset

class Mia:
    """High level interfate for membership inference attack."""
    def __init__(self):
        self.loss_mia = MiaRF()

    def fit(self, data):
        """Fit mia.

        :param data: Datatset with member and non member labeled.
        :type data: fetch_data.Dataset
        """
        self.loss_mia.fit(data)

    def predict(self, data):
        """Add membership status prediction.

        :param data: Dataset with loss.
        :type data: fetch_data.Dataset
        :return: Dataset with predicted membership status.
        :rtype: fetch_data.Dataset
        """
        data = self.loss_mia.predict(data)
        return data

def random_fusion(train, test):
    """Sample as many data points from train as they are in test. Then shuffle the sample and test to obtain a new dataset with as many train examples than test.

    :param train: Member dataset.
    :type train: fetch_data.DataSet
    :param test: Non member dataset.
    :type test: fetch_data.DataSet"""

    testl = test.load()
    trainidx, validation = _pandas_to_dataset(train.load(), return_idx=True)
    
    trainl = (train.load().iloc[trainidx]).sample(n=len(testl),random_state=42,ignore_index=True)
    trainl.insert(loc=0,column="member",value=np.ones(len(trainl)))
    testl.insert(loc=0,column="member",value=np.zeros(len(testl)))
    data = pd.concat([trainl,testl])
    data = data.sample(frac=1,random_state=234,ignore_index=True)


    out = Dataset()
    out.update(data)
    return out

def random_fusion_storage(train,test):
    """Same as mia.random_fusion but for storage dataset.

    :param train: Member dataset.
    :type train: fetch_data.utk.StorageDataset
    :param test: Non member dataset.
    :type test: fetch_data.utk.StorageDataset"""

    n = len(test)
    sub_train = train.extraction(np.random.choice(range(len(train)), size=len(test),replace=False))
    test.x = np.concatenate([test.x,sub_train.x])
    test.y = np.concatenate([test.y,sub_train.y])
    test.member = np.concatenate([np.zeros(n),
                                  np.ones(n)])


    idx = np.linspace(0,len(test)-1,len(test)).astype(int)
    np.random.seed(1234)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    np.random.shuffle(idx)
    test.x = test.x[idx]
    test.y = test.y[idx]
    test.member = test.member[idx]

    return test


