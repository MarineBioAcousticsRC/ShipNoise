import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import concatenate
from keras.utils import np_utils
#CONTINOUS SPEED
import model_gen as mg
from keras import optimizers
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import prepare_data_gen_mixed as pd
import numpy as np 
from DataGenerator import Generator
import unpickle as up


# NOTES: This attempt I am using a mixed data approach 
#
#        This is using the time spectrograms, month, length, average SOG, draught
#        This is running on spectrograms of 512x512 which I think will be standard from now on
#        
#        Doing Percentage loss on this run because it is a regression type model
#        
#        Ran for 65 Epochs:
#        loss: 28.1313 - mean_absolute_error: 419.7307 - val_loss: 21.5098 - val_mean_absolute_error: 320.8754
#   


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.85
sess = tf.Session(config=config)
K.tensorflow_backend.set_session(tf.Session(config=config))
K.tensorflow_backend._get_available_gpus()


folder = "D:\PickledData\\"


# create the MLP and CNN models
mlp = mg.create_mlp(5, regress=False)
cnn = mg.create_cnn(512, 512, 1, regress=False)
 
# create the input to our final set of layers as the *output* of both
# the MLP and CNN
combinedInput = concatenate([mlp.output, cnn.output])
 
# our final FC layer head will have two dense layers, the final one
# being our regression head
x = Dense(4, activation="relu")(combinedInput)
comb_output = (Dense(1,activation='linear', kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x)
 
# our final model will accept categorical/numerical data on the MLP
# input and images on the CNN input, outputting a single value 
model = Model(inputs=[mlp.input, cnn.input], outputs=comb_output)
adam =  optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss="mean_absolute_percentage_error", optimizer=adam,metrics=['mae'])


model.summary()
tensorboard = TensorBoard(log_dir = "/logs/mixed_data_3/")
early_stop= EarlyStopping(monitor = 'val_loss', patience = 3,restore_best_weights=True)

model.fit_generator(generator = pd.data_generator(folder,'train',25),
                    validation_data = pd.data_generator(folder,'test',25),
                    steps_per_epoch=(240),
                    validation_steps=(48),
                    nb_epoch=300,
                    verbose=1,
                    shuffle=True,
                    callbacks=[tensorboard,early_stop])