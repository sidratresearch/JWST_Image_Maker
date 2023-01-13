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

    adjusted = []
    for image in images:
        adjusted.append(curve(image))

    return adjusted


def curve(image):
    """Adjusts the brightness of an image so that the distribution is
    well-spread in the context of being visualized by a 1D colour space.

    Currently, the optimum brightness is so that the mean of the distribution is
    at 1/4th of the brightness spectrum, the standard deviation is 1/16th of
    the spectrum, and the max and min are at the max and min of the spectrum.

    Args:
        image (np.array): 2D image containing flux values to be adjusted

    Returns:
        np.array: adjusted image with brightness "normalized"
    """
    # Setting the desired image constants
    scale = 255.0
    mu_curve, sigma_curve = scale / 8, scale / 16

    # Scaling and clipping the image then calculating mean and standard deviation
    scaled = np.clip(scale * image / np.max(image), 0.0, scale)
    mu, sigma = np.mean(scaled.flatten()), np.std(scaled.flatten())

    curved = np.copy(scaled)

    # Adjusting the brightness nonlinearly by gamma correction
    while not delta(mu, mu_curve):
        curved = gamma(curved, mu / mu_curve)
        mu = np.mean(curved.flatten())

    # Adjusting the contrast linearly by alpha correction (gain)
    while not delta(sigma, sigma_curve):
        curved = alpha(curved, sigma_curve / sigma)
        sigma = np.std(curved.flatten())

    # Adjusting the brightness linearly by beta correction (bias)
    while not delta(mu, mu_curve):
        curved = beta(
            curved, np.sign(mu / mu_curve - 1.0) * np.abs(mu_curve / mu) * mu_curve
        )
        mu = np.mean(curved.flatten())

    plt.figure(figsize=(15, 8))
    plt.subplot(121)
    plt.imshow(scaled, cmap="gray")
    plt.subplot(122)
    plt.imshow(curved, cmap="gray")
    plt.show()

    plt.hist(scaled.flatten(), bins=100, alpha=0.5)
    plt.hist(curved.flatten(), bins=100, alpha=0.5)
    plt.show()

    return curved


def alpha(image, alpha=1.0, scale=255.0):
    """Adjusts an image's contrast by multiplying pixel values by a constant value.

    Args:
        image (np.array): array of pixel values
        alpha (float, optional): contrast value, defaults to 1.0
        scale (float, optional): max brightness value, defaults to 255.0

    Returns:
        np.array: adjusted image
    """
    return np.clip(alpha * image, 0.0, scale)


def beta(image, beta=0.0, scale=255.0):
    """Adjusts an image's brightness by increasing pixel values by a constant value.

    Args:
        image (np.array): array of pixel values
        beta (float, optional): brightness value, defaults to 0.0
        scale (float, optional): max brightness value, defaults to 255.0

    Returns:
        np.array: adjusted image
    """
    return np.clip(image + beta, 0.0, scale)


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
    return np.clip(scale * np.power(image / scale, gamma), 0.0, scale)


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

    adjusted = curves(data)
    return adjusted


data = get_files("/JWST_IMAGE_MAKER/data/test_data_eagle.fits")
curve(data[0][0])
