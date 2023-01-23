import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.esa.jwst import Jwst
import numpy as np
import shutil
import os


def get_query_data(object_name):
    """_summary_

    Args:
        object_name (str): _description_

    Returns:
        _type_: _description_
    """
    query_result = query(object_name)
    get_data(query_result, object_name)
    filenames: list = os.listdir("Query_Data/" + object_name)  # type:ignore

    # Ensuring path information is correct for filenames list
    for i in range(len(filenames)):
        filenames[i] = "Query_Data/" + object_name + "./" + filenames[i]

    return filenames


#%%


def query(object_name):
    """#Querying all JWST data files related to the desired target name

    Args:
        object_name (str): Name of the astronomical object given by the user

    Output:
        query result (Astropy Table): contains all of the information regarding data on that object
    """
    # if RA_dec==True:
    #     ra=np. RA_dec[0]

    target_name = object_name
    target_resolver = "ALL"
    width = u.Quantity(5, u.deg)
    height = u.Quantity(5, u.deg)
    result = Jwst.query_target(
        target_name=target_name,
        target_resolver=target_resolver,
        width=width,
        height=height,
        async_job=True,
    )
    return result


#%%


def get_data(query_result, object_name):
    """This function downloads the 2D image .fits file ('...i2d.fits') for JWST NIRCAM or MIRI data gathered in the query.
    This function is only looking at MIRI data as NIRCAM files are too large (>2 GB)

    Args:
        query result (Astropy Table): contains all of the information regarding data on that object
        object_name (str): Name of the astronomical object given by the user

    Returns:
        Nothing. However, the 2D image .fits files for a given astronomical object is saved in a folder with the following path: ./Query_Data/object_name/'{filename}...i2d.fits'

    """
    # All relevant observation ID's are saved in the miri_obsid list so they can be downloaded. The first choice is NIRCAM data as it contains the most high definition data. If
    # NIRCAM data is unavailable, MIRI data is searched for
    obs_ids = []

    # This list will contain strings denoting which filter (i.e F770W) is used to make a given observation. This list is used to
    # ensure that multiple copies of the same observation are not downloaded

    filters_loaded = []
    NIRCAM = (
        False  # this variable is just used to specify whether NIRCAM data was accessed
    )
    MIRI = False

    first_ra = 0  # this initialization is necessary to ensure the RA and dec of the first fits file selected is not supercded by subsequent iterations in the for loop
    first_dec = 0

    for i in range(len(query_result)):

        instrument_name = query_result[i][5]
        filter = query_result[i][6]

        if (
            instrument_name == "NIRCAM"
        ):  # and 1==0:  # comment out the 1==0 part if you want to use NIRCAM data
            NIRCAM = True
            if filter not in filters_loaded:

                # checking RA and Dec of image taken to ensure the different .fits files gathered are for the same region with a galaxy
                if first_ra == 0 and first_dec == 0:
                    first_ra = query_result[i][8]
                    first_dec = query_result[i][9]

                coord_thresh = 5e-11  # this threshold was determined through trial and error (AKA seeing what produced a well-layered image), try 2e-12 next
                if (
                    np.abs(query_result[i][8] - first_ra) < coord_thresh
                    and np.abs(query_result[i][9] - first_dec) < coord_thresh
                ):

                    # add observation ID to list
                    obs_ids.extend([query_result[i][1]])
                    filters_loaded.extend([query_result[i][6]])

        elif NIRCAM == False and instrument_name == "MIRI":
            MIRI = True
            if filter not in filters_loaded:
                # add observation ID to list
                obs_ids.extend([query_result[i][1]])
                filters_loaded.extend([query_result[i][6]])

    # Downloading relevant fits files from the MIRI observation ID's
    # The relevant file in the product_list folder is the one containing i2d at the end
    # (these are 2D images, for more info see https://jwst-pipeline.readthedocs.io/en/stable/jwst/data_products/science_products.html#i2d)

    #   ****    Right now, this code is just looking at the first observation ID, this should be updated later to sort through relevant folders  *****

    # Creating a new folder for 'i2d.fits' data from query
    newpath = "./Query_Data/" + object_name
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Looping over very first observation ID (this is only to make runtime quicker and needs to be updated to 3 in future)
    for ID in obs_ids[:3]:
        product_list = Jwst.get_product_list(observation_id=ID, product_type="science")

        if type(product_list) == None:
            break

        # Looping over data products to find file ending in 'i2d.fits'
        for name in product_list["filename"]:  # type: ignore
            if "i2d" in name:
                # downloading file and putting it in the desired folder if file doesn't already exist in that path
                if name not in os.listdir(newpath):
                    output_file = Jwst.get_product(file_name=name)
                    shutil.move(output_file, newpath)
    pass

