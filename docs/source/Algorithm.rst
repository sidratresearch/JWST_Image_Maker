Algorithm
=========

This package produces JWST images in 3 main stages. First, the data is imported. This can happen through a query to an online repository of JWST data
or it can import directly from a user's local hard drive. Next, the data is processed to optimize the brightness and contrast of the image
so that all of its features are visible. Finally, the image is plotted with layered colouring to give information about the galaxy at multiple wavelengths.

The main components of the code are 

.. automodule:: JWST_IMAGE_MAKER.main
    :members:

.. automodule:: JWST_IMAGE_MAKER.importing
    :members:

.. automodule:: JWST_IMAGE_MAKER.Astroquery_jwst
    :members:

.. automodule:: JWST_IMAGE_MAKER.processing
    :members:

.. automodule:: JWST_IMAGE_MAKER.plotting
    :members:
