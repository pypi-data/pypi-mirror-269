"""Show how to import the fetch_data package.
If the dataset isn't accessible, it will be downloaded using folktables API.
"""

from ..fetch_data import adult 

def generator(real_data):
    """Return a trained generator."""
    pass

def evaluate(synth_data):
    """Evaluate synthetic data."""
    pass


if __name__ == "__main__":
    #k is the cross-validation step
    #Sensitive is a list containing the sensitive attribute.
    data = adult.load(sensitive=["sex","race"],k=0)

    #To access train/test
    data["train"]
    data["test"]

    synth_data = generator(data["train"])
    evaluate(synth_data)

