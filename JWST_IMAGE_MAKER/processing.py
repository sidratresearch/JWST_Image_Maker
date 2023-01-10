import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt

def process_file(file_data):
    """_summary_

    Args:_type_
        file_data (np.array): array containing data from JWST

    Returns:
        processed_data(np.array): _description_
    """


    # TODO: auto adjust based on distribution, account for all slices
    #       account for biases

    processed_data=file_data

    return processed_data