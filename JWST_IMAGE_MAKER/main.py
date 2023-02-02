from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.Querying import get_query_data
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import plot_data
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# make_image is the function that the user will call
# This function will then call all of the other modules


def make_image(query: bool, save_image: bool, **kwargs):
    """This function creates an image from raw JWST data by calling all of the
    other modules within the package.

    Args:
        query (bool): Determines whether the user wants to gather data automatically using Astro-Query and target object's name. If set to False,
                    the user must pip install JWST_IMAGE_MAKER in a directory that already contains the .fits files that they want to convert into images.

        save_image (bool): Specifies whether the user wants to save the image
            to their computer

    Optional Parameters:
        filename (list of strings): list containing the name(s) of the fits file(s) used to construct an image. Even if only one .fits file is given, it should be stored as a 1 element list. filename must be specified if query=False
        
        object_name (str): string denoting the object's name (e.g. "M16" or "NGC 3132"). This input must be specified if query=True so that the query can actually occur. 

        plot_method (str): This argument specifies how separate images will be combined into 1 image. This is necessary as both the MIRI and NIRCAM instrument take images with different wavelength filters on top. Thus, to get a complete picture, this software combines images with multiple different filters. The valid inputs are "layer" (where the images are stacked on one another to form a single image), "alpha_layer" (where the images are combined using alpha-blending), or "average" (where the flux at each pixel in the overall image is the average of all the images). Default is layer. 

        multi_image (bool): Specifies whether the user wants to see a layered image by stacking observations from multiple wavelengths. If false, this package will output an image from a single observation using a single wavelength filter

    Returns:
        Nothing. There is no variable output for this package. However, it will produce an image and
        save one to the users directory if desired. 
    """
    multi_image: bool = kwargs.get("multi_image", None)
    object_name: str = kwargs.get("object_name", None)
    plot_method: str = kwargs.get("plot_method", None)
    if multi_image == None:
        multi_image = False

    if plot_method == None:
        plot_method = "layer"

    if query == False:
        filenames: list = kwargs.get("filenames", None)
        object_name = filenames[
            0
        ]  # In the case that no object_name is given, set object_name equal to the first file name. This is necessary for plot saving later
    else:
        filenames = get_query_data(object_name, multi_image)

    checking_inputs(query, filenames, object_name)

    file_data: np.ndarray = get_file(filenames)

    processed_data = process_file(file_data)
    plot_data(
        processed_data, filenames, save_image, plot_method, object_name
    )  # this will also save the image
    pass


def checking_inputs(query: bool, filenames: list, object_name: str) -> None:
    """This function ensures that the user has provided the necessary inputs required for the package to perform.

    Args:
        query (bool): see main.make_image description
        filenames (list): see main.make_image description
        object_name (str): see main.make_image description
    """
    if query == True and type(object_name) != str:
        print(
            "ERROR: If query=True, then object_name must be given as a string. It is currently type:",
            type(object_name),
        )

    if query == False and type(filenames) != list:
        print(
            "ERROR: If query=True, then filenames must be given as a list. It is currently type:",
            type(filenames),
        )

    pass
