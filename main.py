from importing import get_file
from processing import process_file
from plotting import plot_data

#make_image is the function that the user will call
#This function will then call all of the other modules

def make_image(filename,save_image):
    """_summary_

    Args:
        filename (str): name of the fits file that the user wants an image of. 

        save_image(T/F): Specifies whether the user wants to save the image to their computer
    """
    file_data=get_file(filename)
    processed_data=process_file(file_data)
    plot_data(processed_data,filename,save_image)  #this will also save the image
    pass  

