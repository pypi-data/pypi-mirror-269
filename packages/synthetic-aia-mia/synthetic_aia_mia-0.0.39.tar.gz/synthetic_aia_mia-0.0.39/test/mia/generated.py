"""Test overfitting with generated noise."""

import unittest
import numpy as np
import pickle
import pandas as pd
import torch
from pathlib import Path

from synthetic_aia_mia.fetch_data import Dataset
from synthetic_aia_mia.experiments.adult_mia import _mia
from synthetic_aia_mia.predictor.adult import AdultNN, _train
from synthetic_aia_mia.aia import Aia
from synthetic_aia_mia.mia import Mia, random_fusion

def generation(step):
    if step=="train":
        N = 100
        x = np.random.uniform(0,1,N)
        y = x>=0.5
    elif step=="test":
        N = 30
        x = np.random.uniform(0,1,N)
        y = x<0.5

    data = np.hstack([x.reshape(-1,1),y.reshape(-1,1)])
    df = pd.DataFrame(data, columns=["x", "PINCP"])
    dset = Dataset()
    dset.update(df)
    return dset


class TestOverfitting(unittest.TestCase):
    def test_overfit_tuning(self):
        train = generation("train")
        test = generation("test")
        mia_data = random_fusion(train, test)
        adultnn = AdultNN(overfit=True, epochs=10, hyper_sample=1, scale=False, loss="entropy")
        adultnn.fit(train)
        pred = adultnn.predict(mia_data)
        mia_metrics = _mia(pred)
        print(mia_metrics)
        return

    #def test_overfit_without_tuning(self):
    #    return
        class scaler:
            def transform(self, x):
                return x
    #    train = generation("train")
    #    test = generation("test")
    #    mia_data = random_fusion(train, test)
        path = Path("debug", "best_config.pickle")
        try :
            with open(path, 'rb') as f:
                config = pickle.load(f)
        except:
            raise ValueError(f"No config specified in {path.resolve()}")

        clf = _train(config, train.load(), stand_alone=True, loss="entropy", epochs=100)
        adultnn = AdultNN()
        adultnn.model = clf
        adultnn.trained = True
        adultnn.columns = ["x"]
        adultnn.scaler = scaler()
        pred = adultnn.predict(mia_data)
        mia_metrics = _mia(pred)
        print(mia_metrics)
