import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
from PIL import Image
from importing2 import get_files  # TODO REMOVE
import os


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

    return np.array(adjusted)


def curve(image, scale=255.0, p=(0.08, 0.998)):
    """Adjusts the brightness of an image so that the distribution is
    well-spread in the context of being visualized by a 1D colour space.

    TODO Expand this descript

    Args:
        image (np.array): 2D image containing flux values to be adjusted
        scale (float, optional): max brightness value, defaults to 255.0
        p (tuple, optional): percentiles to clip to, defaults to 8% and 99.6%

    Returns:
        np.array: adjusted image with auto-optimized brightness and contrast
    """

    # Scaling and clipping the image to account for error pixels
    scaled = np.clip(scale * image / np.max(image), 0.0, scale)
    nonzero = scaled[np.where(scaled > 0)]
    nonmax = nonzero[np.where(nonzero < scale)]

    # Calculating lower and upper percentiles
    lower, upper = np.percentile(nonmax, p[0] * 100), np.percentile(nonmax, p[1] * 100)
    lower_opt, upper_opt = scale * p[0], scale * p[1]

    # Adjusting the brightness linearly by alpha and beta correction
    alpha = (upper_opt - lower_opt) / (upper - lower)
    beta = -alpha * lower
    curved = np.clip(alpha * scaled + beta, 0.0, scale)

    # Adjusting the brightness nonlinearly by gamma correction
    gamma = np.log(np.mean(curved.flatten())) / np.log(scale)
    nonlin = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    fig = plt.figure(figsize=(12, 8), dpi=300)
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.set_title("no corrections")
    ax1.imshow(scaled, cmap="afmhot")
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_title("alpha + beta")
    ax2.imshow(curved, cmap="afmhot")
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_title("gamma")
    ax3.imshow(nonlin, cmap="afmhot")
    ax4 = fig.add_subplot(2, 1, 2)
    ax4.set_title("brightness histogram")
    ax4.hist(
        scaled.flatten(),
        bins=100,
        range=(0, scale),
        alpha=0.5,
        histtype="step",
        label="original",
    )
    ax4.hist(
        curved.flatten(),
        bins=100,
        range=(0, scale),
        alpha=0.5,
        histtype="step",
        ls="--",
        label="linear",
    )
    ax4.hist(
        nonlin.flatten(),
        bins=100,
        range=(0, scale),
        alpha=0.5,
        histtype="step",
        ls=":",
        label="nonlinear",
    )
    ax4.set_yscale("log")
    ax4.legend()
    plt.savefig("JWST_IMAGE_MAKER/figures/eagle_corrections.png")

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


data = get_files("/JWST_IMAGE_MAKER/data/test_eagle.fits")
image = curve(data[0][0])


# im_pil = Image.fromarray(image, mode="F").convert("RGB")
# im_pil.save("JWST_IMAGE_MAKER/figures/test_figures/eagle.jpg")
