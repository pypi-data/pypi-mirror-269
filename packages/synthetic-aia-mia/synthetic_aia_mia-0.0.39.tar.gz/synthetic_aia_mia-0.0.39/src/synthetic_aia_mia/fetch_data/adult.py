"""Load Adult dataset and manage cross validation."""
import folktables 
from folktables import ACSDataSource
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import numpy as np

from . import Dataset
from . import split

def load(sensitive=[],k=0, p=1):
    """Download if necessary folktables adult. Split and return train and test.

    :param sensitive: (Optional default=[]) List of sensitive attributes to include in the features. The sensitive attribute are "sex" and "race".
    :type sensitive: list of str
    :param k: (Optinal default=0) Corss validation step in {0,1,2,3,4}.
    :type k: int
    :param p: Proportion (0<p<=1) of data used.
    :type p: float
    :return: Train and test split dataframes in a dictionary.
    :rtype: Dictionary
    """
    #states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI','ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT','VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR']
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    ca_data = data_source.get_data(states=["CA"],download=True)

    features=[
        'AGEP',
        'COW',
        'SCHL',
        'MAR',
        'OCCP',
        'POBP',
        'RELP',
        'WKHP',
        'PINCP'
    ]
    human_to_census = {"race":"RAC1P","sex":"SEX"}
    for s in sensitive:
        features += [human_to_census[s]]
    ACSIncome = folktables.BasicProblem(features=features,
        target='PINCP',
        target_transform=lambda x: x > 50000,    
        group=['SEX','RAC1P'],
        preprocess=folktables.adult_filter,
        postprocess=lambda x: np.nan_to_num(x, -1),
    )
    ca_features, ca_labels, ca_attrib = ACSIncome.df_to_pandas(ca_data)
    ca_features["PINCP"] = ca_features["PINCP"]>50000
    ca_features.rename({"RAC1P":"race","SEX":"sex"},axis=1,inplace=True)
    ca_features = ca_features.sample(frac=p,replace=False,axis="index", random_state=2134).reset_index()
    data_split = split.split_pandas(ca_features)
    out = {"train":Dataset(),"test":Dataset()}
    out["train"].update(data_split["train"].reset_index(drop=True))
    out["test"].update(data_split["test"].reset_index(drop=True))
    
    return out
