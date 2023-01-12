from JWST_IMAGE_MAKER import make_image
import builtins
import time

def enter():
    pass

def test_checkfiles(capsys,monkeypatch):
    #This function basically checks the entire package by running make_image (which calls every other function)

    path="JWST_IMAGE_MAKER/data/"
    file_name = [
        path+"jw02739-o002_t001_miri_f770w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1500w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    #monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data','input', enter)  #Why this line doesn't work: it looks for a function named input in the plot_data function and tried to get the code to execute the enter function instead (which doesn't even exist)
    monkeypatch.setattr(builtins,'input', lambda x : time.sleep(3))  # This looks for anytime the builtin function 'input' is used and instead of running that line, it executes time.sleep(3)
    make_image(file_name, save_image=False)
    pass


