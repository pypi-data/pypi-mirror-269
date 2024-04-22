"""Experiment module on adult dataset.
It creates the directory results/<generator>/<k> to save three dictionaries of metrics:
    - utility.pickle
    - mia.pickle
    - aia.pickle"""

from pathlib import Path
import pickle
import os
from sklearn.model_selection import StratifiedKFold
import numpy as np
import pandas as pd

from ..fetch_data import utk, Dataset
from ..generator import identity
from ..generator.utk import gan
from ..predictor.utk import UtkNN
from ..aia import Aia
from ..mia import Mia, random_fusion_storage
from ..metrics import balanced_accuracy

import logging

def _aia(storage):
    """Run attribute inference attack on a dataset containing preditions and return attack results.

    :param data: Dataset with prediction as a columne name "hard" and "soft0","soft1", sensitives attributes "sex" and "race", ground truth "PINCP".
    :type data: fetch_data.Dataset
    :return: Attack metrics.
    :rtype: dictionary
    """
    metric_lst = ["balanced_accuracy"]
    metrics = {}
    for attrib in ["sex", "race"]:
        metrics[attrib] = {}
        for labtype in ["hard","soft"]:
            metrics[attrib][labtype] = {}
            for metric in metric_lst:
                metrics[attrib][labtype][metric] = []

    x = np.hstack([storage.soft0.reshape(-1,1),
                    storage.soft1.reshape(-1,1),
                    storage.hard.reshape(-1,1),
                    storage.sex.reshape(-1,1),
                    storage.race.reshape(-1,1)])
    data = pd.DataFrame(x,columns=["soft0",
                                 "soft1",
                                 "hard",
                                 "sex",
                                 "race"])

    skf = StratifiedKFold(random_state=123, shuffle=True)
    for attrib in ["sex","race"]:
        for i,(train,test) in enumerate(skf.split(data,data[attrib])):
            logging.info(f"aia fold {i}")
            data_train = Dataset()
            data_test = Dataset()


            data_train.update((data.iloc[train]).reset_index(drop=True))
            data_test.update((data.iloc[test]).reset_index(drop=True))
            aia = Aia()
            aia.fit(data_train)
            pred = aia.predict(data_test)
            for labtype in ["hard","soft"]:
                for metric in metric_lst:
                    value = balanced_accuracy(pred, attrib, f"{attrib}_{labtype}")
                    metrics[attrib][labtype][metric] += [value]

    return metrics

def _mia(storage):
    """Run membership inference attack on a dataset containing point members and non members with associated logits.

    :para dadata: Dataset with memeber and non memebers labeled.
    :type dadata: fetch_data.Dataset
    :return: Attack metrics.
    :rtype: dictionary
    """

    
    x = np.hstack([storage.loss.reshape(-1,1),
                   storage.member.reshape(-1,1)])
    data = pd.DataFrame(x,columns=["loss","member"])
    skf = StratifiedKFold(shuffle=True,random_state=123)
    data_train = Dataset()
    data_test = Dataset()

    metrics = {"predictor":{"balanced_accuracy":[]},
               "synthetic":{"balanced_accuracy":[]}}
    for i,(train,test) in enumerate(skf.split(data,data["member"])):
        logging.info(f"mia fold {i}")
        data_train.update(data.iloc[train].reset_index(drop=True))
        data_test.update(data.iloc[test].reset_index(drop=True))
        mia = Mia()
        mia.fit(storage.extraction(train))
        pred = mia.predict(storage.extraction(test))
        metrics["predictor"]["balanced_accuracy"] += [balanced_accuracy(pred, "member", "mia")]

        mia_synthetic = mia_syn_utk.UtkNN()
        mia_synthetic.fit(data_train)
        pred = mia.predict(data_test)
        metrics["synthetic"]["balanced_accuracy"] += [balanced_accuracy(pred, "member", "mia_synthetic")]


    return metrics

def _utility(data):
    """Compute utility metrics.

    :param dadata: Dataset containing prediction as an attribute named hard and labels named y.
    :type dadate: fetch_data.utk.StorageDataset
    :return: Utility metrics.
    :rtype: Dictionary
    """

    x = np.hstack([data.y.reshape(-1,1),data.hard.reshape(-1,1)])
    df = pd.DataFrame(x,columns=["y","hard"])
    dset = Dataset()
    dset.update(df)
    metrics = {"ba":balanced_accuracy(dset, "y", "hard")}
    return metrics


def _loop(generator,k):
    """Run in parallel the cross validations steps.
    
    :param generate: A function to generate synthetic data. It takes as an input a dataset and return synthetic data with as many datarecord as in the input.
    :type generate: function
    :param k: Cross validation step.
    :type k: int
    """
    data = utk.load(k=k)

    logging.info(f"generating synthetic data")
    synthetic = generator(data["train"])
    logging.info(f"synthetic data generated")

    logging.info(f"Training predictor")
    utknn = UtkNN()
    utknn.fit(synthetic)
    pred = utknn.predict(data["test"])
    logging.info(f"prediction done")

    with open("pred.pickle", 'wb') as f:
        pickle.dump(pred,f)

    utility_metrics = _utility(pred)
    logging.info(f"utility : {utility_metrics}")

    logging.info("start aia")
    aia_metrics = _aia(pred)
    logging.info(f"aia : {aia_metrics}")

    logging.info("start mia")
    mia_data = random_fusion_storage(data["train"],data["test"])
    pred = utknn.predict(mia_data)
    mia_metrics = _mia(pred)
    logging.info(f"mia : {mia_metrics}")


    path = Path("results",generator.__name__,str(k))
    os.makedirs(path,exist_ok=True)

    with open(Path(path,"utility.pickle"), 'wb') as f:
        pickle.dump(utility_metrics, f)


    with open(Path(path,"aia.pickle"), 'wb') as f:
        pickle.dump(aia_metrics, f)

    with open(Path(path,"mia.pickle"), 'wb') as f:
        pickle.dump(mia_metrics, f)



if __name__=="__main__":
    import logging
    logging.basicConfig(filename='adult.log', level=logging.INFO)
    import sys
    generator_names = {"id":identity,"gan":gan}
    error_message = f"""Invalid command synthax.
Correct synthax is:
python -m synthetic.experiments.adult <generator_name> <k>
where 
    <generator_name> is on of the following:
    {list(generator_names.keys())}

    <k> is the cross validation step in:
    0,1,2,3,4
    """
    try:
        user_argument = sys.argv[1]
    except IndexError:
        raise ValueError(error_message)
        sys.exit()

    try:
        k = int(sys.argv[2])
    except IndexError:
        raise ValueError(error_message)
        sys.exit()

    if not(user_argument in generator_names.keys()):
        raise ValueError(error_message)
        sys.exit()

    if not(k in [0,1,2,3,4]):
        raise ValueError(error_message)
        sys.exit()

    generator = generator_names[user_argument]
    _loop(generator,k=k)



