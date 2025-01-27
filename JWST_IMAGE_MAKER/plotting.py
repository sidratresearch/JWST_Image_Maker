import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from JWST_IMAGE_MAKER.Regridding import regrid_images
from PIL import Image
import numpy as np
import matplotlib
from astropy.io import fits
import glob
import os

"""
This module is responsible for plotting the processed data. It can either plot the average of multiple data sets from different filters
(along with their separate images) or it can plot a layered image. 
"""
#%%Main function that calls other functions based on plot_method specification


def plot_data(
    processed_data: np.ndarray,
    filename: list,
    save_image: bool,
    plot_method: str,
    object_name: str,
):
    """This is the main module and it visualizes the processed data and saves it to the users computer if desired. 

    Args:
        processed_data (np.array):  Data containing the processed JWST data for the desired fits file(s)
        filename (list of strings): contains the names of the data files provided by the user
        save_image (bool): Tells the code whether the user wants the figure to be saved to their computer
        plot_method (str): Specifies whether the produced image will be an average of all the data taken using filters or a layered image
                           where data from each filter is shown using a unique colourmap. Valid string inputs are "Layer","Average", and "alpha layer". "Layer" is the default.
                           
                           Note that the averaging method is very slow as it has to loop over every pixel to check for dark spots (AKA no data spots)
        object_name(str): name of astronomical object being targeted
    """
    print("Plotting beautiful figure")

    regridded_processed_data, old_shape_processed_data = reshaping_data(
        processed_data, filename
    )

    # Selecting plotting method used based on user input
    if plot_method == "Alpha Layer" or plot_method == "alpha layer":
        alpha_layer_images(regridded_processed_data, object_name, save_image)

    elif plot_method == "Average" or plot_method == "average":
        avg_method(regridded_processed_data, object_name, save_image)

    # This is the default method
    elif plot_method == "layer" or plot_method == "Layer":
        simple_layer_method(
            old_shape_processed_data,
            regridded_processed_data,
            object_name,
            save_image,
            filename,
        )

    else:
        print("ERROR: invalid plot_method string given.")
        print("The only valid inputs are layer, Layer, average, and Average")
        print("The user input was ", plot_method)


#%% Emulating Mubdi's jupyter notebook plotting improvements


def simple_layer_method(
    processed_data: np.ndarray,
    new_processed_data: np.ndarray,
    object_name: str,
    save_image: bool,
    filenames: list,
):
    """Stacks the images on top of each other without using alpha-blending.

    Args:
        processed_data (np.ndarray): JWST data array with shape (N,:,:) where N is the number of data files
        new_processed_data (np.ndarray): JWST data array with shape (:,:,N) where N is the number of data files
        object_name (str): name of astronomical object
        save_image (bool): identifies whetehr the user wants a copy of the image saved to their local drive
    """
    # scales the RGB values assigned to each image
    scale_factor = [1.1, 0.9, 1]
    for i, im in enumerate(processed_data):
        tmp_percentile = np.percentile(im.flatten(), [1, 99])

        new_processed_data[:, :, i] = (im - tmp_percentile[0]) / (
            scale_factor[i] * (tmp_percentile[1] - tmp_percentile[0])
        )
    if len(filenames) > 1:
        plotting_script_RGB(new_processed_data, filenames, save_image, object_name)

    else:
        plotting_script(new_processed_data, filenames, save_image, object_name)


def plotting_script(new_processed_data, filenames, save_image, object_name):
    """Contains all of the plotting code necessary to make attractive images and save them
    """
    x = new_processed_data[0, :, 0]
    y = new_processed_data[:, 0, 0]
    extent = 0, len(x), 0, len(y)

    filters_list = get_filter_info(filenames)

    fig = plt.imshow(new_processed_data, extent=extent, cmap="bone")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    black_patch = mpatches.Patch(color="black", label=filters_list[0])
    plt.legend(handles=[black_patch], loc="lower left")
    if save_image == True:
        print("Saving beautiful JWST image to local disk.")
        plt.savefig(
            object_name + ".png",  # type:ignore
            format="png",
            dpi=1200,
            bbox_inches="tight",
        )

    plt.show()


def plotting_script_RGB(new_processed_data, filenames, save_image, object_name):
    """Contains all of the plotting code necessary to make layered RGB images of multiple wavelengths and save them
    """
    x = new_processed_data[0, :, 0]
    y = new_processed_data[:, 0, 0]
    extent = 0, len(x), 0, len(y)

    filters_list = get_filter_info(filenames)

    fig = plt.imshow(new_processed_data, extent=extent)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    red_patch = mpatches.Patch(
        color="red", label="$ \lambda_{\gamma} $=" + filters_list[0][1:-1] + "$\mu m $"
    )
    greenpatch = mpatches.Patch(
        color="green",
        label="$ \lambda_{\gamma} $=" + filters_list[1][1:-1] + "$\mu m $",
    )
    bluepatch = mpatches.Patch(
        color="blue", label="$ \lambda_{\gamma} $=" + filters_list[2][1:-1] + "$\mu m $"
    )
    plt.legend(handles=[red_patch, bluepatch, greenpatch], loc="lower left")
    if save_image == True:
        print("Saving beautiful JWST image to local disk.")
        plt.savefig(
            object_name + ".png",  # type:ignore
            format="png",
            dpi=1200,
            bbox_inches="tight",
        )

    plt.show()


def get_filter_info(filenames: list):
    """Retrieves the wavelength filter value from the header of a given fits file

    Args:
        filenames (list): list of all fits filenames

    Returns:
        list: all of the names of the filters used in collecting the observations
    """
    filter_names_list = []
    headers = [fits.getheader(x, ext=0) for x in filenames]
    for i in range(len(filenames)):
        filter_names_list.append(headers[i].get("Filter"))

    return filter_names_list


def reshaping_data(processed_data, filename):
    """Reshapes the processed_data so that indexing works properly after regridding


    """

    correct_shape_processed_data = np.zeros(
        (
            (
                len(processed_data[0, :, 0]),
                len(processed_data[0, 0, :]),
                len(processed_data[:, 0, 0]),
            )
        )
    )
    for i in range(len(processed_data[:, 0, 0])):
        correct_shape_processed_data[:, :, i] = processed_data[i, :, :]

    # regridding images (i.e aligning them properly in space) if more than one image is given
    if len(filename) > 1:
        regridded_processed_data = regrid_images(
            correct_shape_processed_data, filename
        )  # type:ignore

    else:
        regridded_processed_data = correct_shape_processed_data

    old_shape_pd = np.zeros(
        (
            (
                len(processed_data[:, 0, 0]),
                len(processed_data[0, :, 0]),
                len(processed_data[0, 0, :]),
            )
        )
    )
    for i in range(len(processed_data[:, 0, 0])):
        old_shape_pd[i, :, :] = regridded_processed_data[:, :, i]

    return regridded_processed_data, old_shape_pd


#%% Alpha Layering Method Code


def alpha_layer_images(
    processed_data: np.ndarray, object_name: str, save_image: bool
) -> None:
    """Uses a layering method that involves alpha blending.

     Using alpha blending to combine the different images leads to an oversaturated final image. Think of stacking two 50% translucent windows on each other: you can still kind of see through them, their opacity does not add linearly as you would think to go to 1.


    """

    # cmap_list = ["Reds_r", "YlGn_r", "BuPu_r"] using premade colourmaps
    cmap_list = get_RGB_cmaps()  # using homemade RGB maps
    x = processed_data[0, :, 0]
    y = processed_data[:, 0, 0]
    extent = 0, len(x), 0, len(y)

    for i in range(len(processed_data[0, 0, :])):
        Nslices = len(processed_data[0, 0, :])
        img = processed_data[:, :, i]
        vmin, vmax = np.percentile(
            img.flatten(), [1, 99]
        )  # 12 and 99 were determined by trial and error
        alpha_val = 0.333  # alpha determines the opacity of each layer
        plt.figure(2)
        plt.imshow(
            img, vmin=vmin, vmax=vmax, cmap=cmap_list[i], alpha=alpha_val, extent=extent
        )

    if save_image == True:
        plt.savefig(
            object_name + ".png",  # type:ignore
            format="png",
            dpi=1200,
            bbox_inches="tight",
        )
    plt.show()


#%% Average Flux method


def avg_method(processed_data: np.ndarray, object_name: str, save_image: bool):
    """Takes the average of the 3 images and displays that

    Args:
        processed_data (np.ndarray): array storing the processed JWST data
        object_name (str): name of astronomical object
        save_image (bool): describes whether user wants to save image or not
    """
    stacked_data = stack_images(processed_data)

    # Looping over all data files provided by the user (even if they only provide 1) and making a plot of each
    for i in range(len(processed_data[0, 0, :]) + 1):
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
            # if last iteration, save averaged flux pdf
            if i == len(processed_data[0, 0, :]):
                name = object_name
                new_ext = ".pdf"
                plt.savefig(name + new_ext, format="pdf", dpi=1200, bbox_inches="tight")

    if save_image == False:
        plt.show(block=True)
        # This pause allows the tester to briefly see the images (it is not really necessary for the code though)
        plt.pause(1)

    # Putting in a user input so that images stay visible for as long as the user wants
    if save_image == False:
        input("Press [enter] to close all figures.")

    pass


def stack_images(processed_data: np.ndarray):

    # Generating basic stacked image by taking the average of the pixels across the slices in the processed_data array.
    # Note that each slice in the processed_data array refers to data from a different wavelength filter (and thus different .fits file)
    sum_data = np.zeros((len(processed_data[:, 0, 0]), len(processed_data[0, :, 0])))

    # summing the slices in the array
    for i in range(len(processed_data[0, 0, :])):
        sum_data = processed_data[:, :, i] + sum_data

    # Taking the average of that sum
    avg_data = sum_data / (len(processed_data[0, 0, :]) + 1)  # type:ignore

    # avg_data = ignore_darkspots(processed_data, avg_data)

    return avg_data


def ignore_darkspots(processed_data, avg_data):
    """    This function does the following:

    a. Takes forever to run!!! Like a truly insane amount of time

    b. If a pixel in one of the pictures has a value of zero, do not let that contribute to the average
    i.e if the pixel at index [12,1011] has a value of zero in observations from wavelengths of 770 and 1130 microns,
    only use the information from 1500 micron observation

    The logic behind this is that the zero values are dark spots due to instrumentation error, it doesn't actually mean there is zero
    flux at that wavelength. Thus, this error shouldn't skew my averaged flux.

    

    Args:
        processed_data (np.array): A 2D or 3D numpy array of JWST that has been processed (not exactly sure how yet). The array will be 2D if the user gives a single .fits file and will be 3D otherwise.

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


def get_RGB_cmaps():
    redarr = [(0.0, 0, 0.0), (0.5, 0.5, 0.5), (1.0, 1, 1.0)]

    bluearr = [(0.0, 0.0, 0.0), (0.5, 0.5, 0.5), (1.0, 1.0, 1.0)]

    greenarr = [(0.0, 0.0, 0), (0.5, 0.5, 0.5), (1.0, 1, 1)]

    zero_arr = [(0.0, 0.0, 0), (0.5, 0.0, 0.0), (1.0, 0, 0)]

    red_dict = {"red": redarr, "green": zero_arr, "blue": zero_arr}
    green_dict = {"red": zero_arr, "green": greenarr, "blue": zero_arr}
    blue_dict = {"red": zero_arr, "green": zero_arr, "blue": bluearr}

    green_map = matplotlib.colors.LinearSegmentedColormap(
        "MyColormap", green_dict, N=1e3
    )
    red_map = matplotlib.colors.LinearSegmentedColormap("MyColormap", red_dict, N=1e3)
    blue_map = matplotlib.colors.LinearSegmentedColormap("MyColormap", blue_dict, N=1e3)
    return [red_map, green_map, blue_map]

