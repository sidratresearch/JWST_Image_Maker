import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

"""
This module is responsible for plotting the processed data. It can either plot the average of multiple data sets from different filters
(along with their separate images) or it can plot a layered image. Ultimately, the code should use the layering technique with a customized colour map.

Thus, the next steps for improving this module are going to be:
1. Adding the save_image feature to layer images
2. Make layer_image the default option called in main
2. Add **kwarg to make_image function in main.py that chooses between layering and averaging so that code can still do both in case it needs to
"""


def plot_data(processed_data, filename, save_image):
    """This module visualizes the processed data and saves it to the users computer if desired.

    Args:
        processed_data (np.array): A 2D or 3D numpy array of JWST that has been processed (not exactly sure how yet). The array will be 2D if the user gives a single .fits file and will be 3D otherwise.
        filename (list of strings): contains the names of the data files provided by the user
        save_image (T/F): Tells the code whether the user wants the figure to be saved to their computer
    """

    stacked_data = stack_images(processed_data)

    # Looping over all data files provided by the user (even if they only provide 1) and making a plot of each
    for i in range(len(processed_data[0, 0, :]) + 1):
        print(i)
        # If it is the final loop, show the average of the images provided by the user
        if i == len(processed_data[0, 0, :]):
            img = stacked_data
        else:
            img = processed_data[:, :, i]

        vmin, vmax = np.percentile(
            img.flatten(), [12, 99]
        )  # 12 and 99 were determined by trial and error
        plt.figure(i, figsize=(5, 5), dpi=175)
        plt.imshow(img, vmin=vmin, vmax=vmax, cmap="bone")
        # saving image if desired by user
        if save_image == True:
            if i < len(processed_data[0, 0, :]):
                name = os.path.splitext(filename[i])[0].lower()

            else:
                name = "Flux_Averaged_Image"
            new_ext = ".pdf"
            plt.savefig(name + new_ext, format="pdf", dpi=1200, bbox_inches="tight")

        if save_image == False:
            plt.show(block=False)
            # This pause allows the tester to briefly see the images (it is not really necessary for the code though)
            plt.pause(1)

    # Putting in a user input so that images stay visible for as long as the user wants
    if save_image == False:
        input("Press [enter] to close all figures.")

    pass


def layer_images(processed_data: np.ndarray, filename: list, save_image: bool) -> None:
    cmap_list = ["bone", "afmhot", "copper"]
    x = processed_data[0, :, 0]
    y = processed_data[:, 0, 0]
    extent = 0, len(x), 0, len(y)
    print(extent)

    for i in range(len(processed_data[0, 0, :])):
        Nslices = len(processed_data[0, 0, :])
        alpha_val = 1 / Nslices  # alpha determines the opacity of each layer
        plt.imshow(processed_data[:, :, i], cmap=cmap_list[i], alpha=0.5, extent=extent)

    plt.show()
    plt.savefig("Layering_test", format="pdf", dpi=1200, bbox_inches="tight")


def stack_images(processed_data):
    # Generating basic stacked image by taking the average of the pixels across the slices in the processed_data array.
    # Note that each slice in the processed_data array refers to data from a different wavelength filter (and thus different .fits file)
    sum_data = np.zeros((len(processed_data[:, 0, 0]), len(processed_data[0, :, 0])))

    # summing the slices in the array
    for i in range(len(processed_data[0, 0, :])):
        sum_data = processed_data[:, :, i] + sum_data

    # Taking the average of that sum
    avg_data = sum_data / (len(processed_data[0, 0, :]) + 1)

    avg_data = ignore_darkspots(processed_data, avg_data)

    return avg_data


def ignore_darkspots(processed_data, avg_data):
    """    This function does the following:
    If a pixel in one of the pictures has a value of zero, do not let that contribute to the average
    i.e if the pixel at index [12,1011] has a value of zero in observations from wavelengths of 770 and 1130 microns,
    only use the information from 1500 micron observation

    The logic behind this is that the zero values are dark spots due to instrumentation error, it doesn't actually mean there is zero
    flux at that wavelength. Thus, this error shouldn't skew my averaged flux.

    Args:
        processed_data (np.array): A 2D or 3D numpy array of JWST that has been processed (not exactly sure how yet).
        The array will be 2D if the user gives a single .fits file and will be 3D otherwise.

        avg_data (np.array): a 2D array generated by taking the average of the (potentially) 3D processed_data array

    Returns:
        avg_data (np.array): Identical to above but hopefully the dark spots have been corrected for
    """

    # looping over all rows and columns for each slice to look for dark spots
    for k in range(len(processed_data[0, 0, :])):
        for i in range(len(processed_data[:, 0, 0])):
            for j in range(len(processed_data[0, :, 0])):

                # if a pixel in a given slice is zero (AKA a dark spot), check other slices to see if they have a non-zero pixel in that spot
                if processed_data[i, j, k] == 0:
                    if any(processed_data[i, j, :]) != 0:
                        # find average of non-zero terms
                        sum = 0
                        N = 0
                        for h in range(len(processed_data[0, 0, :])):
                            if processed_data[i, j, h] != 0:
                                # sums the non-zero processed data
                                sum = sum + processed_data[i, j, h]
                                N = (
                                    N + 1
                                )  # N is a counter used to determine the number of non-zero items

                        # replaces the pixel in the avg_data array with one that is unaffected by dark spots (AKA pixels with a brightness value of zero)
                        avg_data[i, j] = sum / N
    return avg_data
