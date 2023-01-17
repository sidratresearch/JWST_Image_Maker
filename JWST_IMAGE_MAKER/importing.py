import numpy as np
from astropy.io import fits
import sys
import os

#path = "JWST_IMAGE_MAKER/JWST_IMAGE_MAKER/data/"


def get_file(filename):
    """This function imports the file provided by the user and converts it to a np.array.
    If the given file does not have a .fits extension, the code will send an error to the user and will not attempt to open the file.

    Args:
        filename (list of strings): A list that contains the name(s) of the fits file(s) that the user wants an image of.

    Returns:
        array_data (np.array): A 3D array containing all of the data for every single .fits file given
    """
    #Checking that input filename(s) are given as a list
    if not isinstance(filename, list):
        raise TypeError(f"was expecting command to be a list, but got a {type(filename)}")

    '''
    # Checking the extension and size of the first filename given by the user
    # Note: this code assumes all given .fits files have the same size
    
    #check_extension(filename[0])  
    #xdim, ydim = check_size(filename[0])
    

    # Creating array that can store the data for ALL of the .fits files provided by the user
    # This array will be 3D to ensure it can store the x-y photon data for each wavelength slice
    full_dataset = np.zeros(((xdim, ydim, len(filename))))
    '''
    largest_index,full_dataset=zeros_array_generator(filename)

    # Looping over all files provided by user and saving their data in full_dataset
    for i in range(len(filename)):
        check_extension(filename[i])
        # Importing fits file
        fits_data = fits.open(filename[i])
        # Converting data from HDUList to np.array
        array_data = fits_data[1].data
        
        if i!=largest_index:
            array_data_pad=full_dataset[:,:,i]  #make empty directory of correct size
            array_data_pad[:array_data.shape[0],:array_data.shape[1]]=array_data  #fill that with data (from smaller dataset)
            array_data=array_data_pad  #change name back so that the next line still works
        
        full_dataset[:, :, i] = array_data
    return full_dataset

def zeros_array_generator(filename):
    """This function creates an array of zeros that has x and y dimensions equal to the largest (most pixelated) fits file image. This allows
       arrays of different sizes to be resized to the correct value by simply appending zeros in the right places

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    xdims=np.zeros(len(filename))
    ydims=np.zeros(len(filename))


    largest_index=0 #this value is used to store the index (within the filename array) of the data set with the largest dimensions

    #This loop is used to determine the dimensions the empty array should have
    for i in range(len(filename)):
        array_data,xdims[i], ydims[i] = check_size(filename[i])
        #checking if arrays have different dimensions, if they do: resize them.
        if i>0:
            if xdims[i]!=xdims[i-1] or ydims[i]!=ydims[i-1]:
                #determining the file with the largest dimensions
                if xdims[i]>xdims[i-1] or ydims[i]>ydims[i-1]:
                    largest_index=i

    fits_data = fits.open(filename[largest_index])
    # Converting data from HDUList to np.array
    array_data = fits_data[1].data

    xdim = len(array_data[:, 0])
    ydim = len(array_data[0, :])

    full_dataset = np.zeros(((xdim, ydim, len(filename))))

    return largest_index,full_dataset



def check_extension(filename):
    """This function checks the extension of a provided data file to ensure it is a .fits

    Args:
        filename (str): name of the specified data file

    Returns:
        void: Stops code if the file is not a .fits file, does nothing otherwise
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
    fits_data = fits.open(filename)
    # Converting data from HDUList to np.array
    array_data = fits_data[1].data
    xdim = len(array_data[:, 0])
    ydim = len(array_data[0, :])
    return array_data, xdim, ydim
