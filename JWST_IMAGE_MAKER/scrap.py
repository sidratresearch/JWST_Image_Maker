import numpy as np

def plusone(x):
    y=x+1
    input("Username: ")
    return y

setattr(plusone,'input','henry')


print(plusone.input)


