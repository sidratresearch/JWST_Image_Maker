from JWST_IMAGE_MAKER.importing import get_file
from JWST_IMAGE_MAKER.processing import process_file
from JWST_IMAGE_MAKER.plotting import alpha_layer_images, plot_data
import numpy as np
import glob
import builtins
import time


def test_simple_layer():
    # inputs
    save_image = True

    fname_list = glob.glob("Query_Data/M16/*")
    file_data = get_file(fname_list)
    processed_data = process_file(file_data)
    plot_data(
        processed_data,
        filename=fname_list,
        save_image=False,
        plot_method="layer",
        object_name="run1",
    )
    assert 1 == 1


def test_alpha_layer():
    # inputs
    save_image = True

    fname_list = glob.glob("Query_Data/M16/*")
    file_data = get_file(fname_list)
    processed_data = process_file(file_data)
    plot_data(
        processed_data,
        filename=fname_list,
        save_image=False,
        plot_method="alpha layer",
        object_name="run1",
    )
    assert 1 == 1


def test_average_method(monkeypatch):
    # inputs
    save_image = True

    fname_list = glob.glob("Query_Data/M16/*")
    file_data = get_file(fname_list)
    processed_data = process_file(file_data)
    monkeypatch.setattr(
        builtins, "input", lambda x: time.sleep(3)
    )  # This looks for anytime the builtin function 'input' is used and instead of running that line, it executes time.sleep(3)
    plot_data(
        processed_data,
        filename=fname_list,
        save_image=False,
        plot_method="average",
        object_name="run1",
    )
    assert 1 == 1

