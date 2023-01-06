import matplotlib.pyplot as plt
import numpy as np
import os

def plot_data(processed_data,filename,save_image):
    """_summary_

    Args:
        processed_data (np.array): Processed data, ideally 2D but can also be 3D. Remember that this will NOT be a multi-row/2-column dataset
    """
    #Add some code here later that makes it look pretty and (maybe) customizes the plotting procedure based on what the image contains

    plt.imshow(processed_data)


    #saving image if desired by user
    if save_image==True:
        name = os.path.splitext(filename)[0].lower()
        new_ext='.pdf'
        plt.savefig(name+new_ext,format='pdf',dpi=1200,bbox_inches='tight')
    pass

