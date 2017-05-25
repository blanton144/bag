import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def asinh_image(image, scale=1.):
    return np.arcsinh(image / scale)


def shim(image, scale=0.1):
    plt.imshow(asinh_image(image, scale=scale),
               interpolation='nearest',
               origin='upper', cmap=cm.gray)
