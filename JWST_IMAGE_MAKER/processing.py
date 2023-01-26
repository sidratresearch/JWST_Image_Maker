import numpy as np
import matplotlib.pyplot as plt


def process_file(images: np.ndarray) -> np.ndarray:
    """Adjusts the brightness of each image within each HUD within each .fits so
    that the distribution is optimized within the displayed colour spectrum.

    I like the way it looks if curve is run twice, it's bad practice but looks good!

    Args:
        images (np.array): array containing data from JWST, collection of 2D flux values

    Returns:
        np.array: array containing flux data adjusted for maximum
        information within middle of displayed spectrum
    """
    curved = []
    for i in range(images.shape[2]):
        curved.append(curve(curve(images[:, :, i])))
    return np.array(curved)


def curve(
    image: np.ndarray, scale: float = 255.0, p: tuple = (0.1, 0.999)
) -> np.ndarray:
    """Adjusts the brightness of an image so that the distribution is well-spread in the context of being visualized by a 1D colour space.

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
    # For Henry - 0 < gamma < 1 makes it brighter, 1 < gamma makes it dimmer
    # 0 < alpha < 1 = contrast decrease, 1 < alpha = contrast increase
    # beta < 0 = brightness decrease, 0 < beta = brightness increase
    # By the ratio between the logarithms of the mean of the image and the scale
    gamma = np.log(np.mean(curved.flatten())) / np.log(scale)
    curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    # By the ratio between the logarithms of the stddev of the image and the scale
    gamma = np.log(scale * 0.341) / np.log(np.std(curved.flatten()))
    curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    # # Just for Henry - 0 to 1 makes it brighter, 1+ makes it dimmer, increasing alpha increases the contrast

    return curved


# Everything below is for fft testing, consider it unimplemented

# REFERENCE
# https://www.eso.org/~ohainaut/images/imageProc.html
# https://iopscience.iop.org/article/10.3847/1538-3881/aaddff/pdf
# https://numpy.org/doc/stable/reference/generated/numpy.hanning.html
# https://numpy.org/doc/stable/reference/generated/numpy.hamming.html
# https://docs.scipy.org/doc/scipy/reference/signal.html

# from importing import get_file
# from matplotlib import pyplot as plt
# from scipy import signal

# Hanning and Hamming functions, look into power spectra cleaning


def denoise(image: np.ndarray, factor: float = 4 * 10 ** -7) -> np.ndarray:
    fhat = np.fft.fft2(image)
    fshift = np.copy(fhat)
    d, r = 1, 0.6
    fshift2 = np.zeros((int(fshift.shape[0] / 2), int(fshift.shape[1] / 2)))
    fshift2[
        d : int(fshift.shape[0] / 2 - d), d : int(fshift.shape[1] / 2 - d)
    ] = fshift[d : int(fshift.shape[0] / 2 - d), d : int(fshift.shape[1] / 2 - d)]
    fshift2[
        int(fshift.shape[0] / 2 * (1 - r)) : int(fshift.shape[0] / 2 * r),
        int(fshift.shape[1] / 2 * (1 - r)) : int(fshift.shape[1] / 2 * r),
    ] = 0
    filtered = np.fft.ifft2(fshift2).real

    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.title("used spectrum")
    plt.imshow(curve(fshift2.real), cmap="gray")
    plt.subplot(122)
    plt.title("filtered image")
    plt.imshow(curve(filtered), cmap="gray")
    plt.show()
    # plt.savefig("JWST_IMAGE_MAKER/figures/processing/denoising/square/eagle.png")
    return filtered


# Projection: astropy WCS
# Then you'll have unaligned multiple frames with WCS coordinates
# Then rebin/regrid to have everything on the same frame to be able to stack
# scipy.ndimage.map_coordinates
