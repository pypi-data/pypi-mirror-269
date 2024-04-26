from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

from ..fetch_data import Dataset

def ctgan(dadata):
    """Generate synthetic data using ctgan trained on input data.

    :param data: Real dataset used to train ctgan.
    :type data: fetch_data.Dataset
    :return: Synthetic dataset.
    :rtype: fetch_data.Dataset
    """

    data = dadata.load()
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data)

    synthesizer = CTGANSynthesizer(metadata)
    synthesizer.fit(data)
    synthetic_data = synthesizer.sample(num_rows=len(data))
    out = Dataset()
    out.update(synthetic_data)
    return out
