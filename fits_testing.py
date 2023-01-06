import numpy as np
from astropy.io import fits

path_data = "data\jw01492-o005_s00004_nirspec_f100lp-g140m-s1600a1-sub2048_cal.fits"
data = fits.open(path_data)
