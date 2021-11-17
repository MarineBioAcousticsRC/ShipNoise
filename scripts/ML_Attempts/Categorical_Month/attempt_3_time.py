import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import Convolution2D, MaxPooling2D, GaussianNoise
from keras.utils import np_utils
#CATEGORICAL MONTH
from keras import optimizers
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import prepare_data_gen as pd
import numpy as np 
from DataGenerator import Generator
import unpickle as up
#sess = tf.Session()
#K.set_session(sess)

# NOTES: This attempt I am trying to guess the month that the ship crossed
#        Gonna mess with Convolutional filters make it 5x5
#        This is using the time spectrograms
#        This is running on spectrograms of 500x500 which I think will be standard from now on
#        
#        
#        Ran for nine Epochs:
#        - 12s - loss: 2.3824 - acc: 0.1920 - val_loss: 2.5062 - val_acc: 0.1375
#        Overfit quickly and never really learned



config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.85
sess = tf.Session(config=config)
K.tensorflow_backend.set_session(tf.Session(config=config))
K.tensorflow_backend._get_available_gpus()


folder = "J:\PickledData\\"
#x_train, x_test, Y_train, Y_test, categories = pd.get_data(folder)
# x_train = np.asarray(x_train)
# x_test = np.asarray(x_test)

#print(x_train.shape)

input_img = Input(shape=(1080,1080,1))
batchsize = 32
# X_train =  x_train.astype('float32')
# X_test = x_test.astype('float32')

# X_train /= np.amax(X_train) #- 0.5
# X_test /= np.amax(X_test) #- 0.5

# x_train = np.reshape(X_train, (-1,501, 501,1))  # adapt this if using `channels_first` image data format
# x_test = np.reshape(X_test, (-1,501, 501,1))  # adapt this if using `channels_first` image data format

# X_train = X_train.reshape((-1,784))
# X_test = X_test.reshape((-1,784))
# print(np.asarray(X_train).shape)

# Y_train = np_utils.to_categorical(y_train, 10)
# Y_test  = np_utils.to_categorical(y_test,10)

x = (Convolution2D(7,7,activation='relu',strides=(2,2),input_shape=(1080,1080,1)))(input_img)
x = (MaxPooling2D(pool_size=(3,3),strides=(2,2)))(x)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (Dropout(0.25))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (Dropout(0.25))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Dropout(0.25))(x)
x = (Flatten())(x)
x = (Dropout(0.5))(x)
x = (Dense(4096, activation='relu'))(x)
x = (Dense(4096, activation='relu'))(x)
classify = (Dense(12,activation='softmax', kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x)


adam =  optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model = Model(input_img,classify)
model.compile(loss='categorical_crossentropy',optimizer=adam,metrics=['accuracy'])
model.summary()
tensorboard = TensorBoard(log_dir = "/logs/time_attempt_3/")
early_stop= EarlyStopping(monitor = 'val_loss', patience = 3,restore_best_weights=True)

#model.load_weights('first_try.h5')
# training_batch_generator = Generator(x_train, Y_train, batchsize)
# validation_batch_generator = Generator(x_test, Y_test, batchsize)



model.fit_generator(generator = pd.data_generator(folder,'train',25),
                    validation_data = pd.data_generator(folder,'test',25),
                    steps_per_epoch=(240),
                    validation_steps=(48),
                    nb_epoch=100,
                    verbose=1,
                    shuffle=True,
                    callbacks=[tensorboard,early_stop])
#score = model.evaluate(X_test, Y_test, verbose=2)
# test_spect = []
# test_months = []
# for ships in up.unpickle_batch(folder,50,6000,6050):
    # for ship in ships:
        # test_spect.append(ship.spect) #GET BATCH DATA
        # test_months.append(ship.month-1)    
    # x_test = np.asarray(test_spect) #PREPARE BATCH DATA
    # x_test =  x_test.astype('float32')
    # x_test /= np.amax(x_test) #- 0.5
    # X_test = np.reshape(x_test, (-1,501, 501,1))
# print(test_months)
# y_prob = model.predict(X_test) 
# y_classes = y_prob.argmax(axis=-1)
# print(y_classes)
# model.save_weights('J:\\scripts\\ML_Attempts\\Weights\\Categorical_Month\\second_try.h5')
# Y_test  = np_utils.to_categorical(test_months,12)
# score = model.evaluate(X_test,Y_test,batch_size=50)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])

