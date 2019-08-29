import numpy as np
np.random.seed(123)
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from matplotlib import pyplot as plt
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import prepare_data as pd
import numpy as np 
sess = tf.Session()
K.set_session(sess)

folder = "D:\PickledData\\"

x_train, x_test, Y_train, Y_test, categories = pd.get_data(folder)
print(x_train.shape)
input_img = Input(shape=(5001,1608, 1))
X_train =  x_train.astype('float32')
X_test = x_test.astype('float32')
X_train /= np.amax(X_train) #- 0.5
X_test /= np.amax(X_test) #- 0.5
x_train = np.reshape(X_train, (len(X_train), 5001, 1608, 1))  # adapt this if using `channels_first` image data format
x_test = np.reshape(X_test, (len(X_test), 5001, 1608, 1))  # adapt this if using `channels_first` image data format
#X_train = X_train.reshape((-1,784))
# X_test = X_test.reshape((-1,784))
print(X_train.shape)

Y_train = np_utils.to_categorical(y_train, 10)
Y_test  = np_utils.to_categorical(y_test,10)

x = (Convolution2D(32,3,3,activation='relu',))(input_img)
x = (Convolution2D(32,3,3,activation='relu'))(x)
x = (MaxPooling2D(pool_size=(2,2)))(x)
x = (Dropout(0.25))(x)
x = (Flatten())(x)
x = (Dense(128,activation='relu'))(x)
x = (Dropout(0.5))(x)
classify = (Dense(categories,activation='softmax' kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x)

model = Model(input_img,classify)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

tensorboard_callback = TensorBoard(log_dir = "/logs/try3/",histogram_freq=1)
early_stop_callback = EarlyStopping(monitor = 'val_loss', patience = 3)

model.fit(x_train,Y_train,batch_size=128,nb_epoch=10,verbose=1,shuffle=True,validation_data=(x_test, Y_test),callbacks=[tensorboard_callback,early_stop_callback])
score = model.evaluate(X_test, Y_test, verbose=2)

model.save_weights('first_try.h5')
print('Test loss:', score[0])
print('Test accuracy:', score[1])

