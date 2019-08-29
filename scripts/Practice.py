import numpy as np
np.random.seed(123)
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard
sess = tf.Session()
K.set_session(sess)

(X_train, y_train), (X_test, y_test) = mnist.load_data()
input_img = Input(shape=(28, 28, 1))
X_train =  X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255 - 0.5
X_train /= 255 - 0.5
x_train = np.reshape(X_train, (len(X_train), 28, 28, 1))  # adapt this if using `channels_first` image data format
x_test = np.reshape(X_test, (len(X_test), 28, 28, 1))  # adapt this if using `channels_first` image data format
#X_train = X_train.reshape((-1,784))
# X_test = X_test.reshape((-1,784))
print(X_train.shape)

Y_train = np_utils.to_categorical(y_train, 10)
Y_test  = np_utils.to_categorical(y_test,10)

x = (Convolution2D(32,9,9,activation='relu',))(input_img)
x = (Convolution2D(32,9,9,activation='relu'))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Dropout(0.25))(x)
x = (Flatten())(x)
x = (Dense(128,activation='relu'))(x)
x = (Dropout(0.5))(x)
classify = (Dense(10,activation='softmax'))(x)
model = Model(input_img,classify)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
tensorboard_callback = TensorBoard(log_dir = "/logs/try2/",histogram_freq=1)
model.fit(x_train,Y_train,batch_size=128,nb_epoch=10,verbose=1,shuffle=True,validation_data=(x_test, Y_test),callbacks=[tensorboard_callback])
score = model.evaluate(x_test, Y_test, verbose=2)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

