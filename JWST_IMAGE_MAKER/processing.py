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

    Currently, the optimum brightness is so that the mean of the distribution is
    at halfway in the brightness spectrum, the standard deviation is 1/8th of
    the spectrum, and the max and min are at the max and min of the spectrum.

    Args:
        image (np.array): 2D image containing flux values to be adjusted

    Returns:
        np.array: adjusted image with brightness "normalized"
    """
    min, max = 0, 255
    mu_curve, sigma_curve = max / 2.0, max / 8.0
    mu, sigma = np.mean(image.flatten()), np.std(image.flatten())
    scaled = image.flatten() * max / np.max(image)

    curved = gamma(image, gamma=sigma / sigma_curve)
    while not delta(sigma, sigma_curve):
        print(sigma)
        sigma = np.std(curved.flatten())
        curved = gamma(image, gamma=sigma / sigma_curve)
        plt.imshow(curved)
        plt.show()

    # TODO delete
    dist = np.histogram(scaled, bins=max, range=(0, max))

    plt.hist(image.flatten(), bins=np.linspace(min, max, 100))
    plt.yscale("log")
    plt.show()
    # end of delete

    return image


def alpha(image, alpha=1.0):
    """Adjusts an image's contrast by multiplying pixel values by a constant value.

    Args:
        image (np.array): array of pixel values
        alpha (float, optional): contrast value, defaults to 1.0

    Returns:
        np.array: adjusted image
    """
    return alpha * image


def beta(image, beta=0.0):
    """Adjusts an image's brightness by increasing pixel values by a constant value.

    Args:
        image (np.array): array of pixel values
        beta (float, optional): brightness value, defaults to 0.0

    Returns:
        np.array: adjusted image
    """
    return beta * image


def gamma(image, gamma=1.0, scale=255.0):
    """Adjusts an image's brightness by increasing pixel values by an
    exponential value. Prevents saturation by scaling brightness differently.

    Args:
        image (np.array): array of pixel values
        gamma (float, optional): adjustment value, defaults to 1.0
        scale (float, optional): max brightness value, defaults to 255.0

    Returns:
        np.array: adjusted image
    """
    return np.power(image / scale, gamma) / scale


def delta(value, constant, delta=0.1):
    """Compares if a value and constant are within a certain fraction of the constant.

    Args:
        value (float): value to compare
        constant (float): constant to be compared with value
        delta (float, optional): fraction of constant which value must be
            within, defaults to 0.1.

    Returns:
        boolean: True if value is within delta of constant, False otherwise
    """
    return np.abs(value - constant) <= delta * constant


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


data = get_files("/JWST_IMAGE_MAKER/data/test_data_eagle.fits")
curve(data[0][0])
