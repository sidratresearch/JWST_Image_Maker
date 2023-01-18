from JWST_IMAGE_MAKER import make_image
import builtins
import time
from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
import numpy as np


def test_importing():
    path = "JWST_IMAGE_MAKER/data/"

    fitsnames = [
        "jw02739-o002_t001_miri_f770w_i2d.fits",
        "jw02739-o002_t001_miri_f1500w_i2d.fits",
        "jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    arr_filename = ["h", "h", "h"]

    for i in range(0, 3):
        arr_filename[i] = path + fitsnames[i]

    full_array = get_file(arr_filename)
    assert isinstance(full_array, np.ndarray) and len(full_array.shape) == 3


def test_processing():
    path = "JWST_IMAGE_MAKER/data/"

    fitsnames = [
        "jw02739-o002_t001_miri_f770w_i2d.fits",
        "jw02739-o002_t001_miri_f1500w_i2d.fits",
        "jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    arr_filename = ["h", "h", "h"]

    for i in range(0, 3):
        arr_filename[i] = path + fitsnames[i]

    full_array = get_file(arr_filename)
    processed_data = process_file(full_array)


"""
I'm commenting this part out as the NIRCAM files are too big to be handled by the computer

def test_NIRCAMfiles():
    #This checks the code's ability to provide plots of the NIRCAM images from JWST

    #This test is currently failing because it says insufficient resources exist to store the fits data in an array
    #it made a really pretty picture though so I think the code itself is solid, the NIRCAM data files are just too damn big


    path="JWST_IMAGE_MAKER/data/"
    file_name = [
        path+"jw02739-o001_t001_nircam_clear-f200w_i2d.fits",
        path+"jw02739-o001_t001_nircam_clear-f187n_i2d.fits"
    ]
    make_image(file_name, save_image=False)

"""
