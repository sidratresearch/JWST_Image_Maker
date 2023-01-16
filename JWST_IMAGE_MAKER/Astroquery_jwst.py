import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.esa.jwst import Jwst
import numpy as np
import shutil
import os

#Querying all JWST data files related to the desired target name
target_name = 'M16'
target_resolver = 'ALL'
width = u.Quantity(5, u.deg)
height = u.Quantity(5, u.deg)
result = Jwst.query_target(target_name=target_name, target_resolver=target_resolver, width=width, height=height, async_job=True)

#Only looking at MIRI data as NIRCAM files are too large (>2 GB)
#All MIRI observation ID's are saved in the miri_obsid list to be saved later
miri_obsid=[]
for i in range(len(result)):
    if 'mirimage' in result[i][1]:
        #print(result[i][1])
        miri_obsid.extend([result[i][1]])

#Downloading relevant fits files from the MIRI observation ID's 
#The relevant file is the one containing i2d at the end (these are 2D images, for more info see https://jwst-pipeline.readthedocs.io/en/stable/jwst/data_products/science_products.html#i2d)


#   ****    Right now, this code is just looking at the first two observation IDs, this should be updated once bones of code are in place  *****

#Creating a new folder for data from Query
newpath = './Query_Data/'+target_name
if not os.path.exists(newpath):
    os.makedirs(newpath)

#Looping over all MIRI observation IDs 
for ID in miri_obsid[:2]:
    product_list=Jwst.get_product_list(observation_id=ID, product_type='science')
    #Looping over data products to find file ending in 'i2d.fits'
    for name in product_list['filename']:
        if 'i2d' in name:
            output_file=Jwst.get_product(file_name=name)
            shutil.move(output_file,newpath+output_file)



