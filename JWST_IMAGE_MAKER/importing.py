import numpy as np
from astropy.io import fits
import sys
import os

path = "JWST_IMAGE_MAKER/JWST_IMAGE_MAKER/data/"


def get_file(filename):
    """This function imports the file provided by the user and converts it to a np.array.
    If the given file does not have a .fits extension, the code will send an error to the user and will not attempt to open the file.

    Args:
        filename (str): name of the fits file that the user wants an image of.

    Returns:
        array_data (np.array): A 3D array containing all of the data for every single .fits file given
    """

    # Checking the extension and size of the first filename given by the user
    # Note: this code assumes all given .fits files have the same size
    check_extension(filename[0])
    xdim, ydim = check_size(filename[0])

    # Creating array that can store the data for ALL of the .fits files provided by the user
    # This array will be 3D to ensure it can store the x-y photon data for each wavelength slice
    full_dataset = np.zeros(((xdim, ydim, len(filename))))

    # Looping over all files provided by user and saving their data in full_dataset
    for i in range(len(filename)):
        check_extension(filename[i])
        # Importing fits file
        fits_data = fits.open(path + filename[i])
        # Converting data from HDUList to np.array
        array_data = fits_data[1].data
        full_dataset[:, :, i] = array_data

    return full_dataset


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


def check_size(filename):
    """This function checks the dimensions of a .fits file

    Args:
        filename (str): name of input .fits file

    returns:
        xdim, ydim (int) : The x and y dimensions of the given .fits files
    """
    fits_data = fits.open(path + filename)
    # Converting data from HDUList to np.array
    array_data = fits_data[1].data
    xdim = len(array_data[:, 0])
    ydim = len(array_data[0, :])
    return xdim, ydim
