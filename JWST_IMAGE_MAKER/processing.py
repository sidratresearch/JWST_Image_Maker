import numpy as np


def process_file(images: np.ndarray) -> np.ndarray:
    """Adjusts the brightness of each image within each HUD within each .fits so
    that the distribution is optimized within the displayed colour spectrum.

    Args:
        images (np.array): array containing data from JWST, collection of 2D flux values

    Returns:
        np.array: array containing flux data adjusted for maximum
        information within middle of displayed spectrum
    """
    curved = []
    for i in range(images.shape[2]):
        curved.append(curve(images[:, :, i]))
    return np.array(curved)


def curve(
    image: np.ndarray, scale: float = 255.0, p: tuple = (0.1, 0.999)
) -> np.ndarray:
    """Adjusts the brightness of an image so that the distribution is
     well-spread in the context of being visualized by a 1D colour space.

    First spreads image distribution over entire brightness spectrum
    [0, ..., scale] based on ratios between desired and initial percentiles.
    Then moves 'useful' information within spectrum up or down based on mean
    of data.

     Args:
         image (np.array): 2D image containing flux values to be adjusted
         scale (float, optional): max brightness value, defaults to 255.0
         p (tuple, optional): percentiles to clip to, defaults to 10% and 99.9%

     Returns:
         np.array: adjusted image with auto-optimized brightness and contrast
    """
    # Scaling and clipping the image to account for error pixels
    scaled = scale * image / np.max(image)
    nonzero = scaled[np.where(scaled != 0)]
    nonmax = nonzero[np.where(nonzero < np.max(nonzero))]

    print(np.min(nonmax), np.max(nonmax), p)

    # Calculating lower and upper percentiles
    lower, upper = np.percentile(nonmax, [p[0] * 100, p[1] * 100])
    lower_opt, upper_opt = scale * p[0], scale * p[1]

    # Adjusting the brightness linearly by alpha and beta correction
    alpha = (upper_opt - lower_opt) / (upper - lower)
    beta = -alpha * lower
    curved: np.ndarray = np.clip(alpha * scaled + beta, 0.0, scale)

    # Adjusting the brightness nonlinearly by gamma correction
    gamma = np.log(np.mean(curved.flatten())) / np.log(scale)
    curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    # Adjusting the brightness nonlinearly by gamma correction (optional)
    gamma = np.log(scale * 0.341) / np.log(np.std(curved.flatten()))
    curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    # # Just for Henry - 0 to 1 makes it brighter, 1+ makes it dimmer, increasing alpha increases the contrast

    # gamma = 1.5
    # curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)
    # alpha = 2.5
    # beta = 0.0
    # curved = np.clip(alpha * curved + beta, 0.0, scale)  # type:ignore

    return curved


# Everything below is for fft testing


def slim(image: np.ndarray) -> np.ndarray:
    power = []
    for xlice in image:
        n = len(xlice)
        fhat = np.fft.fft(xlice, n)
        spectrum = fhat * np.conj(fhat) / n
        indices = spectrum > 100
        clean = spectrum * indices
        fhat = indices * fhat
        ffilt = np.fft.ifft(fhat)
        power.append(np.real(spectrum))
    power = np.array(power)
    plt.imshow(power)
    plt.show()
    return image


from importing import get_file
from matplotlib import pyplot as plt

data = get_file(["JWST_IMAGE_MAKER/data/test_ring.fits"])
image = process_file(data)[0]
slim(image)
