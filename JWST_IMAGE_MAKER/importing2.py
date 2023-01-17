"""
This file has many abilities that importing.py does not. The most important being that 
it can accept both strings and lists of strings. However, when we try to test it, it just runs
forever and never passes or fails.

I think this is due to incompatibility with my plotting script. We will try to get this
importing file to be usable later.


"""


import numpy as np
from astropy.io import fits
import sys
import os

# Some headers of note: PI_NAME, DATE-OBS, TARGPROP, INSTRUME, DURATION


def get_files(filenames):
    """This function calls get_file for every user-input filename.

    Args:
        filenames (list of str): list of user-input filenames

    Returns:
        np.array: array of image collections corresponding to each
        user-input filename
    """
    images = []
    if isinstance(filenames, str):
        images.append(get_file(filenames))
    else:
        for filename in filenames:
            images.append(get_file(filename))
        images_array = np.array(images)
        images_array.reshape(
            (
                (
                    len(images_array[0, :, 0]),
                    len(images_array[0, 0, :]),
                    len(images_array[:, 0, 0]),
                )
            )
        )
        images = images_array
    return images


def get_file(filename):
    """This function attempts to read the user-input .fits file. If the file is
    not a .fits file, the program will terminate.

    Args:
        filename (str): user-input .fits file name

    Returns:
        np.array: array of 2D image data corresponding to passed filename
    """
    check_extension(filename)
    image = []
    file = fits.open(os.getcwd() + filename)
    dim = np.array((file[1].header["NAXIS1"], file[1].header["NAXIS2"]))
    # for hdu in file:
    #     if (
    #         hdu.header["NAXIS"] is not None
    #         and hdu.header["NAXIS"] == 2
    #         and np.array_equal(
    #             np.array((hdu.header["NAXIS1"], hdu.header["NAXIS2"])), dim
    #         )
    #     ):
    # image.append(hdu.data)
    return np.array(file[1].data)


def check_extension(filename):
    """This function checks the extension of a provided data file

    Args:
        filename (str): name of the specified data file
    """
    ext = os.path.splitext(filename)[-1].lower()
    # if the user input file has extension .fits, the code will continue with no problem
    if ext == ".fits":
        pass

    # if the user input file has a different extension, the code will output a warning then stop running
    else:
        print("ERROR: Input file must have a .FITS extension.")
        print("Input File extension is:", ext)
        sys.exit()  # tells code to stop running
