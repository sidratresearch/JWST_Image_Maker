from JWST_IMAGE_MAKER import make_image
from JWST_IMAGE_MAKER.Astroquery_jwst import get_query_data
from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import plot_data
import numpy as np


def test_get_query_data():
    astro_object = "M16"
    filenames = get_query_data(astro_object)
    assert type(filenames) == list
    assert len(filenames) == 1
