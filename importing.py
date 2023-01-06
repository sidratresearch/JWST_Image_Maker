import numpy as np
from astropy.io import fits

import os

def get_file(filename):
    """
    This function imports the file provided by the user. If the given file does not have a .fits extension, the code will send an error 
    to the user and will not attempt to open the file.

    Args:
        filename (str): name of the fits file that the user wants an image of. 

    Returns:
        fits_data (FITS data structure): the raw FITS data from the file given. If a file is given that is unreadable (i.e not a FITS file), return a warning to the user
    """
    path='data/'

    if filename.endswith('.fits')==True:
        fits_data=fits.open(path+filename)
        return fits_data

    else:
        ext = os.path.splitext(filename)[-1].lower()
        print("ERROR: Input file must have a .FITS extension.")
        print('Input File extension is:',ext)
        return 0

    

#test=get_file('test.dat')
test2=get_file('mock_fits_file.fits')