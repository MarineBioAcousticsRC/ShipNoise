import numpy as np
np.random.seed(123)
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import Convolution2D, MaxPooling2D, GaussianNoise
from keras.utils import np_utils
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import prepare_data_month as pd
import numpy as np 
from DataGenerator import Generator

#sess = tf.Session()
#K.set_session(sess)

# NOTES: This attempt I am trying to guess the month that the ship crossed
#        Otherwise this will be identical to attempt 1 of categorical speed
#        Except using the Nadam optimizer to take advantage of Nesterov momentum
#        This is running on spectrograms of 500x500 which I think will be standard from now on
#        
#        
#        Ran for Six Epochs:
#        Final Loss:2.4563 Final Acc:  Final Val_Loss: 2.6156 Final Val_Acc: 0.0982
#        Overfit quickly and never really learned



config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
K.set_session(sess)
K.tensorflow_backend._get_available_gpus()


folder = "J:\PickledData\\"
x_train, x_test, Y_train, Y_test, categories = pd.get_data(folder)
x_train = np.asarray(x_train)
x_test = np.asarray(x_test)

#print(x_train.shape)

input_img = Input(shape=(501,501,1))
batchsize = 32
X_train =  x_train.astype('float32')
X_test = x_test.astype('float32')

X_train /= np.amax(X_train) #- 0.5
X_test /= np.amax(X_test) #- 0.5

x_train = np.reshape(X_train, (-1,501, 501,1))  # adapt this if using `channels_first` image data format
x_test = np.reshape(X_test, (-1,501, 501,1))  # adapt this if using `channels_first` image data format

#X_train = X_train.reshape((-1,784))
# X_test = X_test.reshape((-1,784))
# print(np.asarray(X_train).shape)

# Y_train = np_utils.to_categorical(y_train, 10)
# Y_test  = np_utils.to_categorical(y_test,10)

x = (Convolution2D(32,3,3,activation='relu',input_shape=(501,501,1)))(input_img)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Dropout(0.25))(x)
x = (Flatten())(x)
x = (Dense(128,activation='relu'))(x)
x = (Dropout(0.5))(x)
classify = (Dense(categories,activation='softmax', kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x)

model = Model(input_img,classify)
model.compile(loss='categorical_crossentropy',optimizer='nadam',metrics=['accuracy'])

tensorboard_callback = TensorBoard(log_dir = "/logs/attempt_3/")
early_stop_callback = EarlyStopping(monitor = 'val_loss', patience = 3)

#model.load_weights('first_try.h5')
training_batch_generator = Generator(x_train, Y_train, batchsize)
validation_batch_generator = Generator(x_test, Y_test, batchsize)



model.fit_generator(generator = training_batch_generator,
                    validation_data = validation_batch_generator,
                    steps_per_epoch=(len(x_train) // batchsize),
                    validation_steps=(len(x_test) // batchsize),
                    nb_epoch=20,
                    verbose=2,
                    shuffle=True,
                    callbacks=[tensorboard_callback,early_stop_callback])
#score = model.evaluate(X_test, Y_test, verbose=2)

model.save_weights('J:\\scripts\\ML_Attempts\\Weights\\Categorical_Month\\first_try.h5')
#print('Test loss:', score[0])
#print('Test accuracy:', score[1])

