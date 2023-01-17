from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import plot_data

# make_image is the function that the user will call
# This function will then call all of the other modules


def make_image(filenames, save_image):
    """This function creates an image from raw JWST data by calling all of the
    other modules within this package.

    Args:
        filename (list of strings): list containing the name(s) of the fits
            file(s) used to construct an image. If only one .fits file is given,
            please store as a 1 element list
        save_image (boolean): Specifies whether the user wants to save the image
            to their computer

    Returns:
        This function will never return a variable. It will produce an image and
        save one to the users directory if desired. The code for this can be
        found in the plotting module.
    """
    file_data = get_file(filenames)
    processed_data = process_file(file_data)
    plot_data(processed_data, filenames, save_image)  # this will also save the image
    pass


# Testing the code:

# file_name = [
#     "jw02739-o002_t001_miri_f770w_i2d.fits",
#     "jw02739-o002_t001_miri_f1500w_i2d.fits",
#     "jw02739-o002_t001_miri_f1130w_i2d.fits",
# ]
# make_image(file_name, save_image=False)
