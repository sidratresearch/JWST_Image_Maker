import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import wcs
import glob
from JWST_IMAGE_MAKER import importing
from scipy import ndimage

# main function
def regrid_images(new_processed_data: np.ndarray, filenames: list):
    im_arr: np.ndarray = new_processed_data
    headers = [fits.getheader(x, ext=1) for x in filenames]
    wcs_list = [wcs.WCS(x) for x in headers]
    print(len(wcs_list))
    wcs_corners_list = []

    for i in range(len(filenames)):
        wcs_corners_list.append(
            get_wcs_all_corners(im_arr[:, :, i], wcs_list[i])
        )  # type:ignore

    wcs_corners_arr = np.array(
        wcs_corners_list
    )  # array that holds the RA,dec of all 4 corners in each data set
    print(np.shape(wcs_corners_arr))
    min_ra = np.min(wcs_corners_arr[:, :, 0])
    min_dec = np.min(wcs_corners_arr[:, :, 1])

    max_ra = np.max(wcs_corners_arr[:, :, 0])
    max_dec = np.max(wcs_corners_arr[:, :, 1])

    wcs_grid = np.meshgrid(
        np.linspace(min_ra, max_ra, len(new_processed_data[0, :])),
        np.linspace(min_dec, max_dec, len(new_processed_data[:, 0])),
    )

    im0 = im_arr[:, :, 0]
    px_list = np.meshgrid(np.arange(im0.shape[0]), np.arange(im0.shape[1]))
    radec_list = wcs_list[0].all_pix2world(px_list[0], px_list[1], 0)
    im0_pixcoord = wcs_list[0].all_world2pix(wcs_grid[0], wcs_grid[1], 0)
    reproj_im_0 = ndimage.map_coordinates(im0, im0_pixcoord)

    im1 = im_arr[:, :, 1]
    im1_pixcoord = wcs_list[1].all_world2pix(wcs_grid[0], wcs_grid[1], 0)
    reproj_im_1 = ndimage.map_coordinates(im1, im1_pixcoord)

    im2 = im_arr[:, :, 2]
    im2_pixcoord = wcs_list[2].all_world2pix(wcs_grid[0], wcs_grid[1], 0)
    reproj_im_2 = ndimage.map_coordinates(im2, im2_pixcoord)

    reproj_array = np.stack([reproj_im_0, reproj_im_1, reproj_im_2], axis=-1)

    return reproj_array


# helper functions
def get_all_corner_px(im):
    max_y, max_x = im.shape
    return [[0, 0], [max_y, 0], [max_y, max_x], [0, max_x]]


def get_wcs_all_corners(im, wcs):
    corner_px = get_all_corner_px(im)
    wcs_coord = wcs.all_pix2world(corner_px, 0)
    return wcs_coord

