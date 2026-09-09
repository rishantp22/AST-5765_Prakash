import numpy as np

def rando_func(A, B):
    x = np.linspace(0,1,100)
    y = B* np.sin( 2*np.pi*x/B)
    return y