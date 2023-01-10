import matplotlib.pyplot as plt
import numpy as np
import os

def plot_data(processed_data,filename,save_image):
    """_summary_

    Args:
        processed_data (np.array): Processed data, ideally 2D but can also be 3D. Remember that this will NOT be a multi-row/2-column dataset
    """
    #Add some code here later that makes it look pretty and (maybe) customizes the plotting procedure based on what the image contains

        # showing just the first slice
    for i in range(len(processed_data[0,0,:])): 
        img = processed_data[:,:,i]
        vmin,vmax=np.percentile(img.flatten(), [12,99])  #12 and 99 were determined by trial and error
        plt.figure(i,figsize=(5,5),dpi=175)
        plt.imshow(img, vmin=vmin, vmax=vmax, cmap='bone')
        #saving image if desired by user
        if save_image==True:
            name = os.path.splitext(filename[i])[0].lower()
            new_ext='.pdf'
            path='Figures/'
            plt.savefig(path+name+new_ext,format='pdf',dpi=1200,bbox_inches='tight')
        plt.show()



    pass

