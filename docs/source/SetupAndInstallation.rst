Setup and Installation
======================
The setup process used for this package depends on if the user wants to create images from files they have already downloaded or use querying to access online JWST data. 
The setup is considerably simpler if using querying. However, downloading the data beforehand allows the user to have more choice in what image is actually being created. 
The basic setup procedure is the same for both, with a few extra steps if querying is not desired.

The following instructions assume the user is on a Windows Powershell or Linux based system that already has ``pip`` installed.


**If using the query method:**

*   In the command line, run ``python -m pip install --no-deps JWST-IMAGE-MAKER``

*	Type ``python`` in the command line to enter into a python shell
*	Type ``from JWST_IMAGE_MAKER import make_image``
*   Call the ``make_image`` function in the following way

    *   ``make_image(query=True,save_image=True,object_name='M16')``

    *   Note that in the example above, the user chose to save the image produced by the package and wanted to see an image of galaxy M16.

    *   The saved image will appear in a repository named "M16"

**If downloading the JWST .fits data yourself:**

*	Setup a folder that contains the data files that you want converted to images. In this example, we name this directory JWST_images. These files must have a .fits extension and it is reccommended to get these files from https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
    
    * In the command line, type the following code to make a new directory called "JWST_IMAGES": ``mkdir JWST_images``

    * Move your .fits files (arbitrarily called filename.fits here) into this new directory using the ``mv`` function: ``mv {previous path/filename.fits} {new path/JWST_images/filename.fits}``

*   Navigate into that directory in the command line
    
    * ``cd {new path/JWST_images/filename.fits}``

*	Once you are in that directory, run the following
    
    * ``python -m pip install --no-deps JWST-IMAGE-MAKER``

*	Type ``python`` in the command line to enter into a python shell

    *	Type ``from JWST_IMAGE_MAKER import make_image``

    *	Type ``Filename=[“{filename.fits}”]`` in the python shell. Note that the .fits file names will typically look something like ``jw02739001...i2d.fits``

    *	Note that you can put multiple files within this list. However, even if you are including 1 file, it must be in list format (not a string)

    *	Run ``make_image(query=False, save_Image=True,filenames=Filename)``

    *	The saved image will appear in the same repository your input files are in

*  Enjoy the splendours of our Universe!
