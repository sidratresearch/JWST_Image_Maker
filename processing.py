import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt

def process_file(file_data):
    """_summary_

    Args:_type_
        file_data (FITS data structure): raw FITS file from JWST

    Returns:
        processed_data(np.array): _description_
    """
    # showing just the first slice
    img = file_data[1].data
    vmin,vmax=np.percentile(img.flatten(), [12,99])
    plt.figure(figsize=(5,5),dpi=175)
    plt.imshow(img, vmin=vmin, vmax=vmax, cmap='bone')
    plt.show()

    # TODO: auto adjust based on distribution, account for all slices
    #       account for biases

    processed_data=file_data+5 #hahahahahaha
    return processed_data