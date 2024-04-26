"""Attribute inference attack."""

from finit_classifier import FinitClassifier

from .soft import AiaNN
from .rf import AiaRF

class Hard:
    """Attribute inference attack of hard labels for adult."""
    def __init__(self):
        self.finit = {"race":FinitClassifier(),
                      "sex":FinitClassifier()}
        self.trained = False


    def fit(self, dadata):
        """Fit a finit classifier to predict sensitive attribute from hard labels.

        :param dadata: Auxiliary data for aia training.
        :type dadata: fetch_data.Dataset
        """
        data = dadata.load()
        self.finit["race"].fit(data["hard"].to_numpy().reshape(-1,1), data["race"].to_numpy())
        self.finit["sex"].fit(data["hard"].to_numpy().reshape(-1,1), data["sex"].to_numpy())
        
        self.trained = True

    def predict(self, dadata):
        """Use previously trained finit classifier to infer senstivies attribute and append prediction to input data.

        :param dadata: Auxiliary data for aia evaluation.
        :type dadata: fetch_data.Dataset
        :return: Dataset with aia prediction under the columns "sexAIAhard" and "raceAIAhard".
        :rtype: fetch_data.Dataset
        """
        if not(self.trained):
            raise AssertionError(f"{self} must be trained prioir to predict")
        data = dadata.load()
        data["sex_hard"] = self.finit["sex"].predict(data["hard"].to_numpy().reshape(-1,1))
        data["race_hard"] = self.finit["race"].predict(data["hard"].to_numpy().reshape(-1,1))

        dadata.update(data)
        return dadata


class Soft:
    """Attribute inference attack of soft labels for adult."""
    def __init__(self):
        self.model = {"race":AiaNN(),
                      "sex":AiaNN()}


    def fit(self, dadata):
        """Fit a neural network to predict sensitive attribute from soft labels.

        :param dadata: Auxiliary data for aia training.
        :type dadata: fetch_data.Dataset
        """
        print(dadata.load())
        self.model["race"].fit(dadata, "race")
        self.model["sex"].fit(dadata, "sex")

    def predict(self, dadata):
        """Use previously trained neural network to infer senstivies attribute and append prediction to input data.

        :param dadata: Auxiliary data for aia evaluation.
        :type dadata: fetch_data.Dataset
        :return: Dataset with aia prediction under the columns "sexAIAsoft" and "raceAIAsoft".
        :rtype: fetch_data.Dataset
        """
        dadata = self.model["sex"].predict(dadata)
        dadata = self.model["race"].predict(dadata)
        return dadata

class Aia:
    """High level interface for attribute inference attack. Execute soft and hard attack."""
    def __init__(self):
        self.soft = Soft()
        self.hard = Hard()

    def fit(self, data):
        """Fit aia for hard and soft labels.

        :param data: Dataset containing labels.
        :type data: fetch_data.Dataset
        """
        self.soft.fit(data)
        self.hard.fit(data)

    def predict(self, data):
        """Add sensitive attribute predicton for hard and soft labels.

        :param data: Dataset containing labels.
        :type data: fetch_data.Dataset
        :return: Dataset with predicted sensitive attribute.
        :rtype: fetch_data.Dataset
        """
        data = self.soft.predict(data)
        data = self.hard.predict(data)

        return data


