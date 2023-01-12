import matplotlib.pyplot as plt
import numpy as np
import os

def plot_data(processed_data,filename,save_image):
    """This module visualizes the processed data and saves it to the users computer if desired.

    Args:
        processed_data (np.array): A 2D or 3D numpy array of JWST that has been processed (not exactly sure how yet). The array will be 2D if the user gives a single .fits file and will be 3D otherwise.
        filename (list of strings): contains the names of the data files provided by the user
        save_image (T/F): Tells the code whether the user wants the figure to be saved to their computer
    """
    #Generating basic stacked image by taking the average of the pixels across the slices in the processed_data array.
    #Note that each slice in the processed_data array refers to data from a different wavelength filter (and thus different .fits file)
    sum_data=np.zeros((len(processed_data[:,0]),len(processed_data[0,:])))
    for i in range(len(processed_data[0,0,:])):
        sum_data=processed_data[:,:,i]+sum_data

    avg_data=sum_data/(len(processed_data[0,0,:])+1)
    

    #Looping over all data files provided by the user (even if they only provide 1) and making a plot of each
    for i in range(len(processed_data[0,0,:])+1): 
        print(i)
        #If it is the final loop, show the average of the images provided by the user
        if i==len(processed_data[0,0,:]):
            img=avg_data
        else:
            img = processed_data[:,:,i]

        vmin,vmax=np.percentile(img.flatten(), [12,99])  #12 and 99 were determined by trial and error
        plt.figure(i,figsize=(5,5),dpi=175)
        plt.imshow(img, vmin=vmin, vmax=vmax, cmap='bone')
        #saving image if desired by user
        if save_image==True:
            if i<len(processed_data[0,0,:]):
                name = os.path.splitext(filename[i])[0].lower()
        
            else:
                name='Flux_Averaged_Image'
            new_ext='.pdf'
            plt.savefig(name+new_ext,format='pdf',dpi=1200,bbox_inches='tight')
        plt.show(block=False)
        




    pass

