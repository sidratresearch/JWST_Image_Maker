import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.esa.jwst import Jwst
import numpy as np

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


#   ****    Right now, this code is just looking at the first 5 observations ID, this should be updated once bones of code are in place  *****

for ID in miri_obsid[:5]:
    product_list=Jwst.get_product_list(observation_id=ID, product_type='science')
    for name in product_list['filename']:
        if 'i2d' in name:
            print(name[0])
            output_file=Jwst.get_product(name[0])

print(output_file)


