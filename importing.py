import numpy as np

def get_file(filename):
    """summary

    Args:
        filename (str): name of the fits file that the user wants an image of. 

    Returns:
        fits_file (FITS data structure): the raw FITS data from the file given. If a file is given that is unreadable (i.e not a FITS file), return a warning to the user
    """
    fits_file=np.loadtxt(filename)  #replace this with astropy getfits later
    return fits_file

