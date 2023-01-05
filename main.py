from importing import get_file
from processing import process_file
from plotting import plot_data

def make_image(filename):
    file_data=get_file(filename)
    processed_data=process_file(file_data)
    plot_data(processed_data)  #this will also save the image
    pass  

