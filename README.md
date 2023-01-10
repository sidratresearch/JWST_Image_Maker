# Description of Software Package #
This software package allows a user to create and save images from data gathered by JWST. 

## Installation
1.	Setup a folder that contains the data files that you want converted to images
  a. These files must have a .fits extension. 
  b. It is reccommended to get these files from https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
2.	Once you are in that directory in your command line, run the following
  a.	python -m pip install --index-url https://test.pypi.org/simple/ --no-deps JWST-IMAGE-MAKER
  b.	Or
  c.	python -m pip install --no-deps JWST-IMAGE-MAKER
3.	Type “python” in the command line to enter into a "python shell"
4.	Type “from JWST_IMAGE_MAKER import make_image”
5.	type Filename=[“{your_filename.fits}”]
  a. Note that you can put multiple files within this list. However, even if you are including 1 file, it must be in list format (not a string)
6.	Run “make_image(Filename, save_Image={True/False})”
7.	The saved image will appear in the same repository your input files are in

## Description of Algorithm

## 1. Import

First, we import the file.

## 2. Process

Second, we process the file. 

## 3. Plotting

Third, we visualize the data.

The expected result is a comprehensible and presentable visualization of .fits data.
