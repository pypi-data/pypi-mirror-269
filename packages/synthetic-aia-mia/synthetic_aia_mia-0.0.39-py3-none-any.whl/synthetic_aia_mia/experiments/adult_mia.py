"""Experiment module on ad dataset.
It creates the directory results/<generator>/<k> to save three dictionaries of metrics:
    - utility.pickle
    - mia.pickle
    - aia.pickle"""

from pathlib import Path
import pickle
import os
from sklearn.model_selection import StratifiedKFold

from ..fetch_data import adult, Dataset
from ..generator import identity
from ..generator.adult import ctgan
from ..predictor.adult import AdultNN
from ..aia import Aia
from ..mia import Mia, random_fusion
from ..metrics import balanced_accuracy

import logging

def _mia(dadata):
    """Run membership inference attack on a dataset containing point members and non members with associated logits.

    :para dadata: Dataset with memeber and non memebers labeled.
    :type dadata: fetch_data.Dataset
    :return: Attack metrics.
    :rtype: dictionary
    """

    dadata.save("mia_data.pickle")
    data = dadata.load()
    skf = StratifiedKFold(shuffle=True,random_state=123)
    data_train = Dataset()
    data_test = Dataset()

    metrics = {"balanced_accuracy":[]}
    for i,(train,test) in enumerate(skf.split(data,data["member"])):
        logging.info(f"mia fold {i}")
        data_train.update(data.iloc[train].reset_index(drop=True))
        data_test.update(data.iloc[test].reset_index(drop=True))
        mia = Mia()
        mia.fit(data_train)
        pred = mia.predict(data_test)
        metrics["balanced_accuracy"] += [balanced_accuracy(pred, "member", "mia")]

    return metrics

def _utility(dadata):
    """Compute utility metrics.

    :param dadata: Dataset containing prediction as a column named "hard" and true label (PINCP).
    :type dadate: fetch_data.Dataset
    :return: Utility metrics.
    :rtype: Dictionary
    """

    metrics = {"ba":balanced_accuracy(dadata, "PINCP", "hard")}
    return metrics



def _loop(generator,k,p):
    """Run in parallel the cross validations steps.
    
    :param generate: A function to generate synthetic data. It takes as an input a dataset and return synthetic data with as many datarecord as in the input.
    :type generate: function
    :param k: Cross validation step.
    :type k: int
    :param p: Proportion of dataset used.
    :type p: float in ]0,1]
    """
    data = adult.load(["sex","race"], k=k, p=p)

    logging.info(f"generating synthetic data")
    synthetic = generator(data["train"])
    logging.info(f"synthetic data generated")

    logging.info(f"Training predictor")
    adultNN = AdultNN(overfit=True, hyper_sample=1, scale=False)
    adultNN.fit(synthetic)
    pred = adultNN.predict(data["test"])
    logging.info(f"prediction done")

    utility_metrics = _utility(pred)
    logging.info(f"utility : {utility_metrics}")
    
    logging.info("start mia")
    mia_data = random_fusion(data["train"],data["test"])
    pred = adultNN.predict(mia_data)
    mia_metrics = _mia(pred)
    logging.info(f"mia : {mia_metrics}")

    path = Path("results",generator.__name__,str(k))
    os.makedirs(path,exist_ok=True)

    with open(Path(path,"utility.pickle"), 'wb') as f:
        pickle.dump(utility_metrics, f)

    with open(Path(path,"mia.pickle"), 'wb') as f:
        pickle.dump(mia_metrics, f)



if __name__=="__main__":
    import logging
    logging.basicConfig(filename='adult.log', level=logging.INFO)
    import sys
    generator_names = {"id":identity,"ctgan":ctgan}
    error_message = f"""Invalid command synthax.
Correct synthax is:
python -m synthetic.experiments.adult <generator_name> <k> <p>
where 
    <generator_name> is on of the following:
    {list(generator_names.keys())}

    <k> is the cross validation step in:
    0,1,2,3,4

    <p> is the proportion of data used:
    0<p<=1
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

    try:
        p = float(sys.argv[3])
    except IndexError:
        raise ValueError(error_message)
        sys.exit()


    if not(user_argument in generator_names.keys()):
        raise ValueError(error_message)
        sys.exit()

    if not(k in [0,1,2,3,4]):
        raise ValueError(error_message)
        sys.exit()

    if not(p>0 and p<=1):
        raise ValueError(error_message)
        sys.exit()

    generator = generator_names[user_argument]
    _loop(generator,k=k,p=p)



