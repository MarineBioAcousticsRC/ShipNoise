from keras import regularizers
from keras.layers import Flatten, Input,LSTM,TimeDistributed, concatenate
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Model, Sequential


def create_mlp(dim, regress=True):
    # define our MLP network
    model = Sequential()

    model.add(Dense(512, input_dim=dim))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(256))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(128))
    model.add(Activation("relu"))

    # check to see if the regression node should be added
    if regress:
        model.add(Dense(64, activation="linear"))

    # return our model
    return model

def create_cnn_lstm(n,dim,height,width,depth,filters=(16, 32, 64),regress=False):
    # define our MLP network
    
    # cnn = create_cnn(width, height, depth, filters = filters, regress = True)
    mlp = create_mlp(height)
    # combinedInput = concatenate([mlp.output, cnn.output])

    inputShape = (dim,height)#, width, depth)#
    inputs = Input(shape = inputShape)

    # x = TimeDistributed(mlp)(inputs)
    # x = LSTM(124)(x)
    # x = Dense(124,activation = 'relu')(x)
    # x = Dropout(0.5)(x)
    # x = Dense(124,activation = 'relu')(x)
    # x = Dropout(0.5)(x)
    # x = Dense(124,activation = 'relu')(x)
    # out_0 = Dense(200, name="Speed_0", activation="linear")(x)
    # model = Model(inputs=[mlp.input], outputs=[out_0])
    model = Sequential()
    model.add(TimeDistributed(mlp, input_shape = inputShape))
    model.add(LSTM(64))
    model.add(Dense(64,activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64,activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64,activation = 'relu'))

    model.add(Dense(200, name="Speed_0", activation="linear"))
    model.summary()
    # return our model
    return model

def create_cnn(width, height, depth, filters=(16, 32, 64), regress=False):
    # initialize the input shape and channel dimension, assuming
    # TensorFlow/channels-last ordering
    inputShape = (height, width, depth)
    chanDim = -1

    # define the model input
    inputs = Input(shape=inputShape)

    # loop over the number of filters
    for (i, f) in enumerate(filters):
        # if this is the first CONV layer then set the input
        # appropriately
        if i == 0:
            x = inputs

        # CONV => RELU => BN => POOL
        x = Conv2D(f, (3, 3), padding="same")(x)

        #x = Conv2D(f, (3, 3))(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=-1)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
    # flatten the volume, then FC => RELU => BN => DROPOUT
    x = Flatten()(x)
    x = Dense(64)(x) # was 16
    x = Activation("relu")(x)
    x = BatchNormalization(axis=chanDim)(x)
    x = Dropout(0.5)(x)
    x = Dense(32)(x) # was 16
    x = Activation("relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(16)(x) # was 16
    x = Activation("relu")(x)
    x = Dropout(0.5)(x)

    # apply another FC layer, this one to match the number of nodes
    # coming out of the MLP
    x = Dense(16)(x)
    x = Activation("relu")(x)
    # check to see if the regression node should be added
    if regress:
        x = Dense(1, activation="linear")(x)

    # construct the CNN
    model = Model(inputs, x)

    # return the CNN
    return model


def create_cnn_seq(width, height, depth, filters=(16, 32, 64), regress=False):
    # initialize the input shape and channel dimension, assuming
    # TensorFlow/channels-last ordering
    inputShape = (height, width, depth)
    chanDim = -1
    momentum = .9
    # define the model input
    # inputs = Input(shape=inputShape)
    cnn = Sequential()
    # loop over the number of filters
    for (i, f) in enumerate(filters):
        # if this is the first CONV layer then set the input
        # appropriately
        if i == 0:
            cnn.add(Conv2D(f, (3, 3),activation ='relu',
             padding="same",input_shape = inputShape))
        else:
            cnn.add(Conv2D(f, (3, 3),activation ='relu',padding="same"))

        # CONV => RELU => BN => POOL
        cnn.add(Conv2D(f, (3, 3),activation ='relu',padding="same"))
        cnn.add(BatchNormalization(axis=chanDim,momentum=momentum))
        cnn.add(MaxPooling2D(pool_size=(2, 2)))
    # flatten the volume, then FC => RELU => BN => DROPOUT
    cnn.add(Flatten())
    cnn.add(Dense(64,activation ='relu')) # was 16
    #cnn.add(Activation("relu"))
    cnn.add(BatchNormalization(axis=chanDim,momentum=momentum))
    cnn.add(Dropout(0.5))
    cnn.add(Dense(32,activation ='relu')) # was 16
    cnn.add(Dense(32,activation ='relu')) # was 16
    #cnn.add(Activation("relu"))
    cnn.add(Dropout(0.5))
    cnn.add(Dense(16,activation ='relu')) # was 16
    #cnn.add(Activation("relu"))
    cnn.add(Dropout(0.5))

    # apply another FC layer, this one to match the number of nodes
    # coming out of the MLP
    cnn.add(Dense(16))
    cnn.add(Activation("relu"))
    # check to see if the regression node should be added
    if regress:
        cnn.add(Dense(1, activation="linear"))

    # construct the CNN
    model = cnn# Model(inputs, x)

    # return the CNN
    return model
