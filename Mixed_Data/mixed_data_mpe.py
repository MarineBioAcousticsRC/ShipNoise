#GOAL: CONTINOUS SPEED
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import concatenate
from keras.utils import np_utils
import model_gen as mg
from keras import optimizers
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping
from keras import regularizers
import data_gen_mixed_stand as pd
import numpy as np 
from DataGenerator import Generator
import unpickle as up
import ML_data_collection as dc

#definition of R^2 loss function
def coeff_determination(y_true, y_pred):
    pd.conv(y_true)
    pd.conv(y_pred)
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )


#Command to start TensorBoard:
#tensorboard --logdir=D:\scripts\ML_Attempts\logs\Mixed_Data --host localhost --port 8088

#NUM ATTEMPT:    
num = dc.get_num()

#------------------------------------SETUP-------------------------------------------------------------
#set up the tensorflow backend in order to use gpu 
#only give 85% of gpu over otherwise it crashes
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.85
sess = tf.Session(config=config)
K.tensorflow_backend.set_session(tf.Session(config=config))
K.tensorflow_backend._get_available_gpus()

#source folder of ships
folder = "D:\Pickled_Data_2\\"

# create the MLP and CNN models
mlp = mg.create_mlp(5, regress=False)
cnn = mg.create_cnn(508, 508, 1, filters=(16,32,64), regress=False)
 
# create the input to our final set of layers as the *output* of both
# the MLP and CNN
combinedInput = concatenate([mlp.output, cnn.output])
 
# our final FC layer head will have two dense layers, the final one
# being our regression head
x = Dense(4, activation="relu")(combinedInput)
comb_output = (Dense(1,activation='linear', kernel_regularizer=regularizers.l1_l2(l1 = 0.01,l2 = 0.01)))(x)
 
# our final model will accept categorical/numerical data on the MLP
# input and images on the CNN input, outputting a single value 
model = Model(inputs=[mlp.input, cnn.input], outputs=comb_output)
adam =  optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss="mean_absolute_percentage_error", optimizer=adam,metrics=["mae",coeff_determination])

#-----------------------------------------TRAINING---------------------------------------------------------
#create callbacks one is to display realtime plots on tensorboard
#other stops training if model begins to overfit
model.summary()
tensorboard = TensorBoard(log_dir = 'D:\\scripts\\ML_Attempts\\logs\\Mixed_Data\\mixed_data_{}'.format(num))
early_stop= EarlyStopping(monitor = 'val_loss', patience = 4,restore_best_weights=True)

#train model using data generator in order to conserve memory
mixed = model.fit_generator(generator = pd.data_generator(folder,'train',25),
                    validation_data = pd.data_generator(folder,'test',25),
                    steps_per_epoch=(290),
                    validation_steps=(58),
                    nb_epoch=300,
                    verbose=1,
                    shuffle=True,
                    callbacks=[tensorboard,early_stop])

#save this attempts weights after training                    
model.save_weights('D:\\scripts\\ML_Attempts\\Weights\\Mixed_Data\\attempt_{}.h5'.format(num))

#--------------------------------------DATA COLLECTION--------------------------------------------------------------------------

new_std_dev = pd.get_dev()
percent_from_std_dev = (100 - (mixed.history['val_mean_absolute_error'][-1]/new_std_dev)*100)

feat_array = pd.get_feats()



#this data will be saved in csv with all the other attempts

csv_data = [num,
            feat_array,
            early_stop.stopped_epoch,
            mixed.history['loss'][-1],
            mixed.history['val_loss'][-1],
            pd.conv(mixed.history['mean_absolute_error'][-1]),
            pd.conv(mixed.history['val_mean_absolute_error'][-1]),
            mixed.history['val_coeff_determination'][-1]]

dc.write_data(csv_data,"D:\scripts\ML_Attempts\CSV_Files\Mixed_Data_r2.csv")

#this data will be plotted and the graphs will be saved
# dc.plot_data(num,
            # early_stop.stopped_epoch,
            # mixed.history['loss'],
            # mixed.history['val_loss'],
            # np.asarray(mixed.history['mean_absolute_error'])*conv,
            # np.asarray(mixed.history['val_mean_absolute_error'])*conv)

#predict data and generate residual plot
x_data,true_speeds = pd.one_batch(folder,1000)
print(conv(np.unique(true_speeds)))
print(str(len(np.unique(true_speeds))))
pred_speeds = model.predict(x_data)
pred_speeds_conv = [pd.conv(speed) for speed in pred_speeds] 
pred_speeds_conv = np.unique(pred_speeds_conv)
print(pred_speeds_conv)
print(len(pred_speeds_conv))
# dc.residual_plot(num,true_speeds,pred_speeds_conv)


