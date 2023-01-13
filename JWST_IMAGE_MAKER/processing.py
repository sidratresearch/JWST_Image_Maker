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


def curve(image, scale=255.0, mean_div=8.0, stddev_div=16.0):
    """Adjusts the brightness of an image so that the distribution is
    well-spread in the context of being visualized by a 1D colour space.

    Currently, the optimum brightness is so that the mean of the distribution is
    at 1/8th of the brightness spectrum, the standard deviation is 1/16th of
    the spectrum, and the max and min are at the max and min of the spectrum.

    Intuitively, the greater the mean, the brighter the image, and the greater
    the standard deviation, the more contrast the image has.

    Args:
        image (np.array): 2D image containing flux values to be adjusted
        scale (float, optional): max brightness value, defaults to 255.0
        mean_div (float, optional): divisions to scale to equal mean, defaults to 8.0
        stddev_div (float, optional): divisions to scale to equal stddev, defaults to 16.0

    Returns:
        np.array: adjusted image with brightness "normalized"
    """
    # Setting the desired image constants
    scale = scale
    mu_curve, sigma_curve = scale / mean_div, scale / stddev_div

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


# TODO DELETE, TESTING AREA


def plot_test(sp, image, md, sd):
    curved = curve(image, mean_div=md, stddev_div=sd)
    plt.subplot(sp)
    plt.imshow(curved, cmap="bone")
    plt.title(
        f"mean={np.mean(curved.flatten()):.1f} ({md:.0f} divisions) \n stddev={np.std(curved.flatten()):.1f} ({sd:.0f} divisions)"
    )
    return curved


data = get_files("/JWST_IMAGE_MAKER/data/test_data_eagle.fits")

image = data[0][0]
scale = 255.0
scaled = np.clip(scale * image / np.max(image), 0.0, scale)

plt.figure(figsize=(16, 8))
plt.subplot(241)
plt.imshow(scaled, cmap="bone")
plt.title(
    f"mean={np.mean(scaled.flatten()):.2f} stddev={np.std(scaled.flatten()):.2f}\noriginal"
)
c1 = plot_test(242, image, 9.0, 12.0)
c2 = plot_test(243, image, 8.0, 13.0)
c3 = plot_test(244, image, 7.0, 14.0)
c4 = plot_test(245, image, 6.0, 15.0)
c5 = plot_test(246, image, 5.0, 16.0)
c6 = plot_test(247, image, 4.0, 17.0)
c7 = plot_test(248, image, 3.0, 18.0)
plt.show()

# plt.hist(scaled.flatten(), bins=100, alpha=0.2)
# plt.hist(c1.flatten(), bins=100, alpha=0.2)
# plt.hist(c2.flatten(), bins=100, alpha=0.2)
# plt.hist(c3.flatten(), bins=100, alpha=0.2)
# plt.hist(c4.flatten(), bins=100, alpha=0.2)
# plt.hist(c5.flatten(), bins=100, alpha=0.2)
# plt.hist(c6.flatten(), bins=100, alpha=0.2)
# plt.hist(c7.flatten(), bins=100, alpha=0.2)
# plt.yscale("log")
# plt.show()
