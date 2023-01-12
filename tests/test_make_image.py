from JWST_IMAGE_MAKER import make_image

def test_checkfiles(capsys,monkeypatch):
    #This function basically checks the entire package by running make_image (which calls every other function)

    path="JWST_IMAGE_MAKER/data/"
    file_name = [
        path+"jw02739-o002_t001_miri_f770w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1500w_i2d.fits",
        path+"jw02739-o002_t001_miri_f1130w_i2d.fits",
    ]
    #setattr('JWST_IMAGE_MAKER.plotting.plot_data','input', 'enter')
    monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data','input', 'enter')  #Both this line and the one below result in "no attribute input in str"
    #monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data.input', lambda: 'enter')  # "JWST...plot_data has no attribute input" even though that is what I'm hoping this line will do!!
    make_image(file_name, save_image=False)
    pass

# def test_prompt(capsys, monkeypatch):
#     #This function checks 
#     monkeypatch.setattr('JWST_IMAGE_MAKER.plotting.plot_data', lambda: 'no')
#     val = make_image(file_name, save_image=False)
#     assert not val
