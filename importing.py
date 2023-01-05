import numpy as np

def get_file(filename):
    """summary

    Args:
        filename (str): name of the fits file that the user wants an image of. 

    Returns:
        _type_: _description_ hello
    """
    fits_file=np.loadtxt(filename)  #replace this with astropy getfits later
    return fits_file

