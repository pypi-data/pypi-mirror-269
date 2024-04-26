import unittest
import pandas as pd
import numpy as np

from synthetic_aia_mia.mia import random_fusion
from synthetic_aia_mia.predictor.adult import _pandas_to_dataset
from synthetic_aia_mia.fetch_data import Dataset

class TestFusion(unittest.TestCase):
    """Test if fusion of train and test dataset works."""
    def test_fusion(self):
        print("\n")
        N = 100
        data = np.random.uniform(0,1000,[N,2])
        for i in range(N):
            data[i,1] = i%2

        train_np = data[:int(0.8*N)]
        test_np = data[int(0.8*N):]


        train = Dataset()
        df = pd.DataFrame(train_np, columns=["x", "PINCP"])
        #print(df)
        train.update(df)
        test = Dataset()
        test.update(pd.DataFrame(test_np, columns=["x", "PINCP"]))
        #Simulate validation split in _train()
        traintrain, trainval = _pandas_to_dataset(train.load())
        traintrain = traintrain.x.numpy()
        traintrain = traintrain.reshape(len(traintrain))
        trainval = trainval.x.numpy()
        trainval = trainval.reshape(len(trainval))

        fusion = random_fusion(train,test)
        ful = fusion.load()
        ful0 = ful[ful["member"]==0]["x"]
        fun0 = ful0.to_numpy()
        ful1 = ful[ful["member"]==1]["x"]
        fun1 = ful1.to_numpy()
        fun = ful["x"].to_numpy()
        self.assertEqual(len(ful),0.4*N)

        i = 0
        def compare(a,b):
            eps = 0.001
            return np.abs(a-b) <= eps

        for a in range(len(fun1)):
            out = False
            for b in range(len(traintrain)):
                out = out or compare(traintrain[b], fun1[a])
                #out = out or (str(round(traintrain[b],0))==str(round(fun1[a],0)))
            if not(out):
                i += 1
                print(fun1[a])
            self.assertTrue(out)
            self.assertTrue(i/N<=5/1000)

        test = test.load()["x"].to_numpy()

        for a in range(len(test)):
            out = False
            for b in range(len(fun0)):
                out = out or compare(test[a], fun0[b])
                #out = out or (str(round(test[a],3))==str(round(fun0[b],3)))
            self.assertTrue(out)

        for a in range(len(trainval)):
            out = True
            for b in range(len(fun)):
                out = out and not(compare(trainval[a], fun[b]))
                #out = out and (str(round(trainval[a],3))!=str(round(fun[b],3)))

                if str(round(trainval[a],3))==str(round(fun[b],3)):
                    print("--------------------------")
                    print(trainval[a])
                    print(fun[b])
                    print("--------------------------")
            self.assertTrue(out)


