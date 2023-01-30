from JWST_IMAGE_MAKER import processing
import numpy as np
import pytest


@pytest.fixture
def size():
    return (10, 10)


@pytest.fixture
def noise(size):
    return np.random.gumbel(size=size)


def test_curve_noise(noise, size):
    processed = processing.curve(noise)
    assert processed.shape == size and not np.array_equal(processed, noise)


def test_curve_range(noise):
    processed = processing.curve(noise)
    assert np.max(processed) != np.max(noise) and np.min(processed) != np.min(noise)


@pytest.mark.xfail
def test_process_file(noise, size):
    processed = processing.process_file(noise)
    assert processed.shape == (size)


@pytest.mark.xfail
def test_process_file_list(noise):
    images = np.array([noise, noise, noise])
    processed = processing.process_file(images)
    assert len(processed) == 3
