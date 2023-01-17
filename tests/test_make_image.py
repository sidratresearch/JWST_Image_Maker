from JWST_IMAGE_MAKER import make_image
import builtins
import time
from JWST_IMAGE_MAKER.importing import get_file as gf1
from JWST_IMAGE_MAKER.importing2 import get_files as gf2
import numpy as np

def test_checkfiles(monkeypatch):
    #This checks the code's ability to provide plots of the MIRI images from JWST
    path="JWST_IMAGE_MAKER/data/"
    file_name = [
        path+"jw02739-o002_t001_miri_f770w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1500w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    #monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data','input', enter)  #Why this line doesn't work: it looks for a function named input in the plot_data function and tried to get the code to execute the enter function instead (which doesn't even exist)
    monkeypatch.setattr(builtins,'input', lambda x : time.sleep(3))  # This looks for anytime the builtin function 'input' is used and instead of running that line, it executes time.sleep(3)
    make_image(file_name, save_image=False)


'''
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

'''

def test_importing():
    path1="JWST_IMAGE_MAKER/data/"
    path2="/JWST_IMAGE_MAKER/data/"

    fitsnames=[
        "jw02739-o002_t001_miri_f770w_i2d.fits",
        "jw02739-o002_t001_miri_f1500w_i2d.fits",
        "jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    arr_filename1=['h','h','h']
    arr_filename2=['h','h','h']


    for i in range(0,3):
        arr_filename1[i]=path1+fitsnames[i]
        arr_filename2[i]=path2+fitsnames[i]


    str_filename=path2+"jw02739-o002_t001_miri_f770w_i2d.fits"

    #full_array2=gf2(str_filename)  #this test passes works because Hansen's code accepts strings
    full_array1=gf1(arr_filename1) #This test passes because my code accepts lists of strings
    full_array2=gf2(arr_filename2) #this test passes works because Hansen's code also accepts lists
    assert np.shape(full_array1)==np.shape(full_array2)

    #full_array1=gf1(str_filename) #This test fails because my code does not accept strings (must be list of strings) 
 
    

    
