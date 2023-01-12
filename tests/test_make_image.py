from JWST_IMAGE_MAKER import make_image

def test_checkfiles():
    path="JWST_IMAGE_MAKER/data/"
    file_name = [
        path+"jw02739-o002_t001_miri_f770w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1500w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    make_image(file_name, save_image=False)
    