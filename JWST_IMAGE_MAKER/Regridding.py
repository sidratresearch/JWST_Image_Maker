import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import wcs
import glob
from JWST_IMAGE_MAKER import importing
from scipy import ndimage

# main function
def regrid_images(new_processed_data: np.ndarray, filenames: list):
    """This function aligns different images in space based on their WCS coordinates. It aligns them by regridding the images and putting each image at the proper RA-dec pixel on an image

    Args:
        new_processed_data (np.ndarray): a 3D array containing the JWST data for 3 separate observations
        filenames (list): list of filenames for the different images

    Returns:
        np.ndarray: the reprojected version of the input arrays
    """

    # Get the headers and WCS coordinates for each observation
    headers = [fits.getheader(x, ext=1) for x in filenames]
    wcs_list = [wcs.WCS(x) for x in headers]

    # Gathering the RA-dec information for each corner of each observation
    wcs_corners_list = []
    for i in range(len(filenames)):
        wcs_corners_list.append(
            get_wcs_all_corners(new_processed_data[:, :, i], wcs_list[i])
        )

    wcs_corners_arr = np.array(wcs_corners_list)

    # Storing the minimum and maximum RA and dec in order to make a grid large enough to accomadate each of the 3 seprate images
    min_ra = np.min(wcs_corners_arr[:, :, 0])
    min_dec = np.min(wcs_corners_arr[:, :, 1])

    max_ra = np.max(wcs_corners_arr[:, :, 0])
    max_dec = np.max(wcs_corners_arr[:, :, 1])

    wcs_grid = np.meshgrid(
        np.linspace(min_ra, max_ra, len(new_processed_data[0, :])),
        np.linspace(min_dec, max_dec, len(new_processed_data[:, 0])),
    )

    # Using astropy.allworld2pix to map all of the different coordinate systems to a common grid
    im0 = new_processed_data[:, :, 0]  # this image contains new_processed_data
    im0_pixcoord = wcs_list[0].all_world2pix(wcs_grid[0], wcs_grid[1], 0)
    reproj_im_0 = ndimage.map_coordinates(im0, im0_pixcoord)

    im1 = new_processed_data[:, :, 1]
    im1_pixcoord = wcs_list[1].all_world2pix(wcs_grid[0], wcs_grid[1], 0)
    reproj_im_1 = ndimage.map_coordinates(im1, im1_pixcoord)

    im2 = new_processed_data[:, :, 2]
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

