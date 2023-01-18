from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.Astroquery_jwst import get_query_data
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import plot_data
import numpy as np

# make_image is the function that the user will call
# This function will then call all of the other modules


def make_image(query: bool, save_image: bool, **kwargs):
    """This function creates an image from raw JWST data by calling all of the
    other modules within this package.

    Args:
        query (bool): Determines whether the user wants to gather data automatically by inputting their target object's name

        save_image (bool): Specifies whether the user wants to save the image
            to their computer

    Kwargs:
        filename (list of strings): list containing the name(s) of the fits
            file(s) used to construct an image. If only one .fits file is given,
            please store as a 1 element list. This must be specified if query=False

        
        object_name (str): string denoting the object's name. Must be specified if query=True so that the query can actually occur

        plot_method (str): can be "layer" or "average". Default is layer

    Returns:
        This function will never return a variable. It will produce an image and
        save one to the users directory if desired. The code for this can be
        found in the plotting module.
    """
    object_name: str = kwargs.get("object_name", None)
    plot_method: str = kwargs.get("plot_method", None)
    if plot_method == None:
        plot_method = "layer"

    if query == False:
        filenames: list = kwargs.get("filenames", None)
        object_name = filenames[
            0
        ]  # In the case that no object_name is given, set object_name equal to the first file name. This is necessary for plot saving later
    else:
        filenames = get_query_data(object_name)

    checking_inputs(query, filenames, object_name)

    file_data: np.ndarray = get_file(filenames)

    processed_data = process_file(file_data)
    plot_data(
        processed_data, filenames, save_image, plot_method, object_name
    )  # this will also save the image
    pass


def checking_inputs(query: bool, filenames: list, object_name: str) -> None:
    if query == True and type(object_name) != str:
        print(
            "ERROR: If query=True, then object_name must be given as a string. It is currently",
            type(object_name),
        )

    if query == False and type(filenames) != list:
        print(
            "ERROR: If query=True, then filenames must be given as a list. It is currently",
            type(filenames),
        )

    pass


# Testing the code:

# file_name = [
#     "jw02739-o002_t001_miri_f770w_i2d.fits",
#     "jw02739-o002_t001_miri_f1500w_i2d.fits",
#     "jw02739-o002_t001_miri_f1130w_i2d.fits",
# ]
# make_image(file_name, save_image=False)
