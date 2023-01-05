import matplotlib.pyplot as plt
import numpy as np

def plot_data(processed_data):
    """_summary_

    Args:
        processed_data (np.array): Processed data, ideally 2D but can also be 3D. Remember that this will NOT be a multi-row/2-column dataset
    """
    plt.imshow(processed_data)
    plt.savefile('change_this_later.pdf')
    pass