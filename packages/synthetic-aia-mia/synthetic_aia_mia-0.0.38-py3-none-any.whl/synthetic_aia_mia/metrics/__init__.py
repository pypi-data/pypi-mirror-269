"""Metrics"""
import numpy as np

def balanced_accuracy(dset, y, yhat):
    """Compute the blanced accuracy.

    :param dset: Data with label and predictions.
    :type dest: fetch_data.Dataset
    :param y: Key for label.
    :type y: str
    :param yhat: Key for prediction.
    :type: str
    :return: Balanced accuracy.
    :rtype: float
    """ 

    data = dset.load()
    yhat_val = data[yhat].to_numpy()
    y_val = data[y].to_numpy()
    ba = np.mean([np.mean(yhat_val[y_val==yy]==yy) for yy in np.unique(y_val)])
    return ba
