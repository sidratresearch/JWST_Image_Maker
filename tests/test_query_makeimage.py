from JWST_IMAGE_MAKER import make_image
import builtins
import time
from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
import numpy as np
import glob


# def test_makeimage():
#     fname_list = glob.glob("Query_Data/M16/*")
#     make_image(query=False, save_image=False, filenames=fname_list, plot_method="layer")
#     assert 1 == 1


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


def test_querytrue():
    make_image(query=True, save_image=False, object_name="M16", multi_image=True)
