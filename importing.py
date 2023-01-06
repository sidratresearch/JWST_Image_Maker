import numpy as np
from astropy.io import fits
import sys
import os

def get_file(filename):
    """
    This function imports the file provided by the user. If the given file does not have a .fits extension, the code will send an error 
    to the user and will not attempt to open the file.

    Args:
        filename (str): name of the fits file that the user wants an image of. 

    Returns:
        fits_data (FITS data structure): the raw FITS data from the file given. Note: the code will not return this if an improper input file is given.
    """
    path='data/'

    #Checking extension of user input file
    ext = os.path.splitext(filename)[-1].lower()

    if ext == '.fits':
        fits_data=fits.open(path+filename)
        return fits_data

    else:
        print("ERROR: Input file must have a .FITS extension.")
        print('Input File extension is:',ext)
        sys.exit()  #tells code to stop running 

    
#Testing functionality
test=get_file('test.dat')
test2=get_file('mock_fits_file.fits')