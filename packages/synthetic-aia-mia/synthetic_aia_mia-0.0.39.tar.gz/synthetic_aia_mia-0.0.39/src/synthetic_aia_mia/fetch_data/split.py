"""Split data into train / test using 5 folding corss validation."""
import numpy as np
from sklearn.model_selection import StratifiedKFold

def split_numpy(data,k=0):
    """5-folding of dataset dictionary of numpy array.

    :param data: Dataset where each key maps to a numpy array.
    :type data: Dictionary
    :param k: (Optional) Indice of the fold, can be 0,1,2,3 or 4.
    :type k: int 
    :return: Dataset with train and test.
    :rtype: Dictionary
    """
    keys = list(data.keys())
    n = np.shape(data[keys[0]])[0]
    idx = np.linspace(0,n-1,n).astype(int)
    test = (idx[int(k*0.2*(n))]<=idx)&(idx<=idx[int((k+1)*0.2*(n-1))])
    train = ~test
    data_split = {"train":{},"test":{}}
    for key in keys:
        data_split["train"][key] = data[key][train]
        data_split["test"][key] = data[key][test]

    return data_split

def split_pandas(data,k=0):
    """5-folding of dataset dictionary of numpy array.

    :param data: Dataset in the form of a dataframe.
    :type data: pandas.dataframe
    :param k: (Optional) Indice of the fold, can be 0,1,2,3 or 4.
    :type k: int 
    :return: Dataset with train and test.
    :rtype: Dictionary
    """

    skf = StratifiedKFold(random_state=1234,shuffle=True)
    for i,(tmp_train,tmp_test) in enumerate(skf.split(data,data["PINCP"])):
        if i==k:
            train = tmp_train
            test = tmp_test

    data = {"train":data.iloc[train],
            "test":data.iloc[test]}

    return data

