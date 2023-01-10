import numpy as np
from astropy.io import fits
import sys
import os

path = "JWST_IMAGE_MAKER/data/"


def get_files(filenames):
    """This function calls get_file for every user-input filename.

    Args:
        filenames (list of str): list of user-input filenames

    Returns:
        img_book (np.array): array of image collections corresponding to each
        user-input filename
    """
    img_book = np.array([])
    for filename in filenames:
        np.append(img_book, get_file(filename))
    return img_book


def get_file(filename):
    """This function attempts to read the user-input .fits file. If the file is
    not a .fits file, the program will terminate.

    Args:
        filename (str): user-input .fits file name

    Returns:
        set (np.array): array of 2D image data corresponding to passed filename
    """
    check_extension(filename)
    file = fits.open(os.getcwd() + filename)
    img = np.array([])
    for hdu in file:
        if hdu.header["NAXIS"] is not None and hdu.header["NAXIS"] == (2,):
            np.append(img, hdu.data)
    return img


def check_extension(filename):
    """This function checks the extension of a provided data file

    Args:
        filename (str): name of the specified data file

    Returns:
        void: Stops code if the file is not a .fits file, nothing otherwise
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
