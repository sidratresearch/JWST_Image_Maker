import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.esa.jwst import Jwst
import numpy as np
import shutil
import os


def get_query_data(object_name: str):
    """_summary_

    Args:
        object_name (str): _description_

    Returns:
        _type_: _description_
    """
    query_result = query(object_name)
    get_MIRI_data(query_result, object_name)
    filenames: list = os.listdir("Query_Data/" + object_name)

    # Ensuring path information is correct for filenames list
    for i in range(len(filenames)):
        filenames[i] = "Query_Data/" + object_name + "./" + filenames[i]

    return filenames


#%%


def query(object_name: str):
    """#Querying all JWST data files related to the desired target name

    Args:
        object_name (str): Name of the astronomical object given by the user

    Output:
        query result (Astropy Table): contains all of the information regarding data on that object
    """

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


def get_MIRI_data(query_result, object_name):
    """This function downloads the 2D image .fits file ('...i2d.fits') for JWST MIRI data gathered in the query.
    This function is only looking at MIRI data as NIRCAM files are too large (>2 GB)

    Args:
        query result (Astropy Table): contains all of the information regarding data on that object
        object_name (str): Name of the astronomical object given by the user

    Returns:
        Nothing. However, the 2D image .fits files for a given astronomical object is saved in a folder with the following path: ./Query_Data/object_name/'{filename}...i2d.fits'

    """
    # All MIRI observation ID's are saved in the miri_obsid list so they can be downloaded
    miri_obsid = []

    # This list will contain strings denoting which filter (i.e F770W) is used to make a given observation. This list is used to
    # ensure that multiple copies of the same observation are not downloaded

    filters_loaded = []

    for i in range(len(query_result)):
        instrument_name = query_result[i][5]
        filter = query_result[i][6]

        if instrument_name == "MIRI":
            if filter not in filters_loaded:
                # add observation ID to list
                miri_obsid.extend([query_result[i][1]])
                filters_loaded.extend([query_result[i][6]])

    # Downloading relevant fits files from the MIRI observation ID's
    # The relevant file in the product_list folder is the one containing i2d at the end
    # (these are 2D images, for more info see https://jwst-pipeline.readthedocs.io/en/stable/jwst/data_products/science_products.html#i2d)

    #   ****    Right now, this code is just looking at the first observation ID, this should be updated later to sort through relevant folders  *****

    # Creating a new folder for 'i2d.fits' data from query
    newpath = "./Query_Data/" + object_name
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    print("miri_obsid", miri_obsid)

    # Looping over very first observation ID (this is only to make runtime quicker and needs to be updated in future)
    for ID in miri_obsid[:1]:
        product_list = Jwst.get_product_list(observation_id=ID, product_type="science")

        if type(product_list) == None:
            break

        # Looping over data products to find file ending in 'i2d.fits'
        for name in product_list["filename"]:  # type: ignore
            print("name:", name)
            if "i2d" in name:
                # downloading file and putting it in the desired folder if file doesn't already exist in that path
                if name not in os.listdir(newpath):
                    output_file = Jwst.get_product(file_name=name)
                    shutil.move(output_file, newpath)
    pass

