from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import layer_images, plot_data
import numpy as np


def test_layer_images():
    # inputs
    save_image = True

    path = "JWST_IMAGE_MAKER/data/"
    filenames = [
        path + "jw02739-o002_t001_miri_f770w_i2d.fits",
        path + "jw02739-o002_t001_miri_f1500w_i2d.fits",
        path + "jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    file_data = get_file(filenames)
    processed_data = process_file(file_data)

    plot_data(
        processed_data,
        filename=filenames,
        save_image=True,
        plot_method="average",
        object_name="wowee",
    )
    assert 1 == 1

    # layer_images(processed_data, object_name="test", save_image=True)  # this will also save the image
