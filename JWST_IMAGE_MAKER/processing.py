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

    return curved


# Everything below is for fft testing

from importing import get_file
from matplotlib import pyplot as plt

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def denoise(image: np.ndarray, factor: float = 4 * 10**-3) -> np.ndarray:
    smushed = np.copy(image)
    for i in range(len(smushed)):
        xlice = smushed[i]
        fhat = np.fft.fft(xlice)
        threshold = np.max(fhat) * factor
        fhat[np.where(np.abs(fhat) < threshold)[0]] = 0
        ff = np.real(np.fft.ifft(fhat))
        smushed[i] = ff
    for j in range(len(smushed[0])):
        ylice = smushed[:, j]
        fhat = np.fft.fft(ylice)
        threshold = np.max(fhat) * factor
        fhat[np.where(np.abs(fhat) < threshold)[0]] = 0
        ff = np.real(np.fft.ifft(fhat))
        for i in range(len(smushed)):
            smushed[i, j] = ff[i]
    return smushed


data = get_file(["JWST_IMAGE_MAKER/data/test_galaxy2.fits"])
image = process_file(data)[0]
smushed = denoise(image)
plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.title("Adjusted Image")
plt.imshow(image, cmap="copper")
plt.subplot(132)
plt.title("Denoised Image")
plt.imshow(smushed, cmap="copper")
plt.subplot(133)
plt.title("Enhanced Differences")
plt.imshow(curve(image - smushed), cmap="copper")
plt.savefig("JWST_IMAGE_MAKER/figures/processing/denoise_failure_galaxy2.png")
