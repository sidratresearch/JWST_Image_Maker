import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.1.5"
PACKAGE_NAME = "JWST_IMAGE_MAKER"
AUTHOR = "Henry White and Hansen Jiang"
AUTHOR_EMAIL = "henrywhite@sidratresearch.com, hansen@sidratresearch.com"
URL = "https://github.com/henrywhite2727/JWST_Image_Maker"

LICENSE = "Apache License 2.0"
DESCRIPTION = "Creates images from raw JWST data"
# LONG_DESCRIPTION = (HERE / "README.md").read_text()
# LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    "numpy",
    "astropy",
    "astroquery",
    "scipy",
    "matplotlib",  # maybe remove .pyplot later
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    # long_description=LONG_DESCRIPTION,
    # long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)

