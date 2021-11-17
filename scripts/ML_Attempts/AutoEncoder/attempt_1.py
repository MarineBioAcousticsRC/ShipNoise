#AUTOENCODER
import unpickle as up
import numpy as np
np.random.seed(123)
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import Conv2D, MaxPooling2D, GaussianNoise, UpSampling2D
from keras.utils import np_utils
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import prepare_data_encoder as pd
import numpy as np 
from DataGenerator import Generator

#sess = tf.Session()
#K.set_session(sess)
folder = "J:\PickledData\\"
# NOTES: This attempt I am trying to create encoded representations of the the spectrograms
#        This is running on spectrograms of 500x500 which I think will be standard from now on
#        My goal is to be able to add more data to the spectrogram and to take some of the load off
#        of the second neural net
#        
#        Ran for  Epochs:
#        Final Loss: Final Acc:  Final Val_Loss:  Final Val_Acc: 
#        Overfit quickly and never really learned



config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
K.set_session(sess)
K.tensorflow_backend._get_available_gpus()


folder = "J:\PickledData\\"
# x_train, x_test, Y_train, Y_test, categories,ships = pd.get_data(folder)
# x_train = np.asarray(x_train)
# x_test = np.asarray(x_test)

#print(x_train.shape)

input_img = Input(shape=(500,500,1))
# batchsize = 32
# X_train =  x_train.astype('float32')
# X_test = x_test.astype('float32')

# X_train /= np.amax(X_train) #- 0.5
# X_test /= np.amax(X_test) #- 0.5

# x_train = np.reshape(X_train, (-1,501, 501,1))  # adapt this if using `channels_first` image data format
# x_test = np.reshape(X_test, (-1,501, 501,1))  # adapt this if using `channels_first` image data format

#X_train = X_train.reshape((-1,784))
# X_test = X_test.reshape((-1,784))
# print(np.asarray(X_train).shape)

# Y_train = np_utils.to_categorical(y_train, 10)
# Y_test  = np_utils.to_categorical(y_test,10)

x = Conv2D(16, (3, 3), activation='relu', padding='same', input_shape = (500,500,1))(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(16, (3, 3), activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adamax', loss='binary_crossentropy')
autoencoder.summary()
tensorboard_callback = TensorBoard(log_dir = "/logs/auto_attempt_1/")
early_stop_callback = EarlyStopping(monitor = 'val_loss', patience = 3)

#model.load_weights('first_try.h5')
# training_batch_generator = Generator(x_train, x_train, batchsize)
# validation_batch_generator = Generator(x_test, x_test, batchsize)



autoencoder.fit_generator(generator = pd.data_generator(folder,'train'),
                    validation_data = pd.data_generator(folder,'test'),
                    steps_per_epoch=(120),
                    validation_steps=(24),
                    nb_epoch=20,
                    verbose=1,
                    shuffle=True,
                    callbacks=[tensorboard_callback,early_stop_callback])
#score = model.evaluate(X_test, Y_test, verbose=2)

model.save_weights('J:\\scripts\\ML_Attempts\\Weights\\AutoEncoder\\first_try.h5')
#print('Test loss:', score[0])
#print('Test accuracy:', score[1])


encoder = Model(input_layer, encoding_layer)
for ships in unpickle_batch(folder,50,0,50):
    for ship in ships:
        test_spect.append(ship.spect) #GET BATCH DATA
    x_test = np.asarray(test_spect) #PREPARE BATCH DATA
    x_test =  x_test.astype('float32')
    x_test /= np.amax(x_test) #- 0.5
    X_test = np.reshape(x_test, (-1,501, 501,1))
    for i in range(len(ships)):
        encodings = encoder.predict(X_test)
        ships[i].encoded = encodings[i]
        

    up.store(ships,folder)