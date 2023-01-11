import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
from importing2 import get_files  # TODO REMOVE


def curves(images):
    """Adjusts the brightness of each image within each HUD within each .fits so
    that the distribution is optimized within the displayed colour spectrum.

    Args:_type_
        images (np.array): array containing data from JWST, collection of 2D flux values

    Returns:
        np.array: array containing flux data adjusted for maximum
        information within middle of displayed spectrum
    """

    return images_curved


def curve(image):
    """Adjusts the brightness of an image so that the distribution is
    well-spread in the context of being visualized by a 1D colour space.

    Args:
        image (np.array): 2D image containing flux values to be adjusted

    Returns:
        np.array: adjusted image with brightness "normalized"
    """

    alpha, beta, gamma = 1.0, 0.0, 1.0

    scale = 255 / np.max(image)
    dist = np.hist(image * scale, bins=255, range=(0, 255))

    plt.show()

    return image_curved


def process_file(data):
    """Processes passed .fits data (in the form of np.arrays) by adjusting the
    brightness.

    Args:
        data (np.array): data created by the importing module from the
        user-input .fits file.

    Returns:
        np.array: the processed data
    """

    return data_pro


get_files("/data/test_data_eagle.fits")
