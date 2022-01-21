import keras
from keras import layers

# This is the size of our encoded representations
# For me I wanted the encoding dim down to 1
encoding_dim = 1  # 1 float -> compression of factor 5

# This is our input image
input_img = keras.Input(shape=(5,))
# "encoded" is the encoded representation of the input
encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = layers.Dense(5, activation='sigmoid')(encoded)

### AUTOENCODER ###
# This model maps an input to its reconstruction
autoencoder = keras.Model(input_img, decoded)

### ENCODER ###
# This model maps an input to its encoded representation
encoder = keras.Model(input_img, encoded)

### DECODER ###
# This is our encoded (32-dimensional) input
encoded_input = keras.Input(shape=(encoding_dim,))
# Retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# Create the decoder model
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))

autoencoder.compile(optimizer='adam', loss='mean_squared_error')