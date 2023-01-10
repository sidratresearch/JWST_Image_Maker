import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
import os

eagle = fits.open("JWST_IMAGE_MAKER/data/test_data_eagle.fits")

print(eagle.info())

try:
    os.remove("JWST_IMAGE_MAKER/test.txt")
except:
    print("no text file")

f = open("JWST_IMAGE_MAKER/test.txt", "a")

for hdu in eagle:
    f.write("new\n")
    headers = hdu.header
    for header in headers:
        f.write(header)
        f.write(":\t")
        f.write(headers.comments[header])
        f.write("\n")

f.close()


def show(data):
    plt.imshow(data)
    plt.show()


# Some headers of note: PI_NAME, DATE-OBS, TARGPROP, INSTRUME, DURATION
