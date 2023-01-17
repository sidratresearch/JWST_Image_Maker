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

    adjusted = []
    for image in images:
        adjusted.append(curve(image))

    return np.array(adjusted)


def curve(
    image: np.ndarray, scale: float = 255.0, p: tuple = (0.08, 0.998)
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
         p (tuple, optional): percentiles to clip to, defaults to 8% and 99.8%

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
    curved: np.ndarray = np.clip(alpha * scaled + beta, 0.0, scale)

    # Adjusting the brightness nonlinearly by gamma correction
    gamma = np.log(np.mean(curved.flatten())) / np.log(scale)
    curved = np.clip(scale * np.power(curved / scale, gamma), 0.0, scale)

    return curved
