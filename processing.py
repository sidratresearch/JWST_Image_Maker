def process_file(file_data):
    """_summary_

    Args:_type_
        file_data (FITS data structure): raw FITS file from JWST

    Returns:
        processed_data(np.array): _description_
    """
    
    processed_data=file_data+5
    return processed_data