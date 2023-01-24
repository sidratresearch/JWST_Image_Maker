from JWST_IMAGE_MAKER import make_image
import builtins
import time
from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
import numpy as np


def test_NIRCAM():
    path = [
        "Query_Data/M16/jw02739001001_02101_00005_nrcb4_i2d.fits",
        "Query_Data/M16/jw02739001001_02103_00005_nrcalong_i2d.fits",
        "Query_Data/M16/jw02739001004_04101_00002_nrcb3_i2d.fits",
    ]
    make_image(query=False, save_image=False, filenames=path)


# def test_queryfalse(monkeypatch):
#     # This checks the code's ability to provide plots of the MIRI images from JWST
#     path = "JWST_IMAGE_MAKER/data/"
#     file_name = [
#         path + "jw02739-o002_t001_miri_f770w_i2d.fits",
#         path + "jw02739-o002_t001_miri_f1500w_i2d.fits",
#         path + "jw02739-o002_t001_miri_f1130w_i2d.fits",
#     ]
#     # monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data','input', enter)  #Why this line doesn't work: it looks for a function named input in the plot_data function and tried to get the code to execute the enter function instead (which doesn't even exist)
#     monkeypatch.setattr(
#         builtins, "input", lambda x: time.sleep(3)
#     )  # This looks for anytime the builtin function 'input' is used and instead of running that line, it executes time.sleep(3)
#     make_image(query=False, save_image=False, filenames=file_name)


# def test_querytrue():
#     make_image(query=True, save_image=False, object_name="M16")
