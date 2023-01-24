Algorithm
=========

This package produces JWST images in 3 main stages. First, the data is imported. This can happen through a query to an online repository of JWST data
or it can import directly from a user's local hard drive. Next, the data is processed to optimize the brightness and contrast of the image
so that all of its features are visible. Finally, the image is plotted with layered colouring to give information about the galaxy at multiple wavelengths.

.. toctree::
   :maxdepth: 3
   :caption: Modules:

   Importing
   Querying
   processing
   plotting

The main software that calls all of these separate modules is explained below.

.. automodule:: JWST_IMAGE_MAKER.main
    :members:


