from keras.layers import Dense, Flatten, Reshape, Conv2D, UpSampling2D, \
                         Cropping2D, MaxPool2D
from keras.models import Sequential

__author__ = "Hanna Go"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Hanna Go"
__email__ = "hannago2917@gmail.com"
__status__ = "Development"

def simple_cae(input_shape, latent_dim, initializer, act="elu"):
    encoder = Sequential()

    decoder = Sequential()

    return encoder, decoder