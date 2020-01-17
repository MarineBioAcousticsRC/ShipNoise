#GOAL: CONTINOUS SPEED
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation,Flatten
from keras.layers import concatenate
from keras.utils import np_utils
import model_gen as mg
from keras import optimizers
import tensorflow as tf
from keras import backend as K
from keras.callbacks import TensorBoard,EarlyStopping, PrintCallback
from keras import regularizers
import data_gen_mixed_stand_vector_with_dist as pd
import numpy as np 
from DataGenerator import Generator
import unpickle as up
import ML_data_collection as dc
from custom_losses import r_2,conv_mae_0,conv_mae_100,conv_mae_200,RMSE_0,RMSE_100,RMSE_200,euclidean_distance_loss
# from custom_callbacks import print_callback



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
mlp_feat = mg.create_mlp(5, regress=False)
cnn = mg.create_cnn(508, 508, 1, filters=(16,32,64), regress=False)
mlp_dist = mg.create_mlp(6, regress=False) 

# create the input to our final set of layers as the *output* of both
# the MLP and CNN
combinedInput = concatenate([mlp_feat.output, cnn.output, mlp_dist.output])
 
# our final FC layer head will have two dense layers, the final one
# being our regression head
x = Dense(4, activation="relu")(combinedInput)

x_0 = Dense(4, activation="relu")(x)
x_100 = Dense(4, activation="relu")(x)
x_200 = Dense(4, activation="relu")(x)

out_0 = (Dense(1,activation='linear', name="Speed_0", kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x_0)
out_100 = (Dense(1,activation='linear', name="Speed_100", kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x_100)
out_200 = (Dense(1,activation='linear', name="Speed_200", kernel_regularizer=regularizers.l1_l2(l1 = 0.001,l2 = 0.001)))(x_200)
# our final model will accept categorical/numerical data on the MLP
# input and images on the CNN input, outputting a single value 
model = Model(inputs=[mlp_feat.input, cnn.input, mlp_dist.input], outputs=[out_0,out_100,out_200])
#adam is the default loss function and I see no reason to change it
#lowered learning rate to debug remember to set it back to 0.0001
adam =  optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

#Compile model and define all metrics different depths have different conversions therfore each
#must be converted differently unlike in the single depth model
#switched loss to euclidean_distance_loss may switch back to ['mae','mae','mae']
model.compile(loss=['mae','mae','mae'], optimizer=adam,metrics={'Speed_0': [conv_mae_0,r_2,RMSE_0],
                                                                'Speed_100': [conv_mae_100,r_2,RMSE_100], 
                                                                'Speed_200': [conv_mae_200,r_2,RMSE_200]})                                       
#-----------------------------------------TRAINING---------------------------------------------------------
#create callbacks one is to display realtime plots on tensorboard
#other stops training if model begins to overfit
model.summary()
tensorboard = TensorBoard(log_dir = 'D:\\scripts\\ML_Attempts\\logs\\Mixed_Data\\mixed_data_vector_{}'.format(num))
early_stop= EarlyStopping(monitor = 'val_loss', patience = 5,restore_best_weights=True)
print_callback = PrintCallback()
# remote_monitor = RemoteMonitor()

#train model using data generator in order to conserve memory
mixed = model.fit_generator(generator = pd.data_generator(folder,'train',25),
                    validation_data = pd.data_generator(folder,'test',25),
                    steps_per_epoch=(290),
                    validation_steps=(58),
                    nb_epoch=300,
                    verbose=0,
                    shuffle=True,
                    callbacks=[tensorboard,early_stop,print_callback])

#save this attempts weights after training                    
model.save_weights('D:\\scripts\\ML_Attempts\\Weights\\Mixed_Data_Vector\\attempt_{}.h5'.format(num))
json_model = model.to_json()
dc.write_json('D:\\scripts\\ML_Attempts\\JSON\\Mixed_Data_Vector\\attempt_{}.txt'.format(num),json_model)
model.save('D:\\scripts\\ML_Attempts\\Saved_Models\\Ship_Noise_Mixed_Data_{}'.format(num))
#--------------------------------------DATA COLLECTION--------------------------------------------------------------------------

feat_array = pd.get_feats()

#this data will be saved in csv with all the other attempts
#find best epoch and use that data as that epochs weights are the ones saved.
min_in = mixed.history['val_loss'].index(min(mixed.history['val_loss']))


csv_data = [num,
            feat_array,
            early_stop.stopped_epoch,
            mixed.history['val_Speed_0_conv_mae_0'][min_in],
            mixed.history['val_Speed_100_conv_mae_100'][min_in],
            mixed.history['val_Speed_200_conv_mae_200'][min_in],
            mixed.history['val_Speed_0_RMSE_0'][min_in],
            mixed.history['val_Speed_100_RMSE_100'][min_in],
            mixed.history['val_Speed_200_RMSE_200'][min_in],
            mixed.history['val_Speed_0_r_2'][min_in],
            mixed.history['val_Speed_100_r_2'][min_in],
            mixed.history['val_Speed_200_r_2'][min_in]]

dc.write_data(csv_data,"D:\scripts\ML_Attempts\CSV_Files\Mixed_Data_Multi_Depth.csv")

# this data will be plotted and the graphs will be saved
# dc.plot_data(num,
        # early_stop.stopped_epoch,
        # mixed.history['loss'],
        # mixed.history['val_loss'],
        # np.asarray(mixed.history['mean_absolute_error'])*conv,
        # np.asarray(mixed.history['val_mean_absolute_error'])*conv)

#predict data and generate residual plot


x_data,true_speeds,dates = pd.eval_batch(folder,200)
pred_speeds = model.predict(x_data)

pred_0 = []
pred_100 = []
pred_200 = []


for i in range(len(pred_speeds[0])):
    pred_0.append(pd.conv(pred_speeds[0][i][0],0))
for i in range(len(pred_speeds[1])):
    pred_100.append(pd.conv(pred_speeds[1][i][0],1))
for i in range(len(pred_speeds[2])):
    pred_200.append(pd.conv(pred_speeds[2][i][0],2))
    
#convert all speeds for plotting
true_0 = pd.conv(true_speeds[0],0)
true_100 = pd.conv(true_speeds[1],1)
true_200 = pd.conv(true_speeds[2],2)

conv_true = [true_0,true_100,true_200]
conv_pred = [pred_0,pred_100,pred_200]
print(conv_true)
print(len(np.unique(conv_true)))
print(conv_pred)
print(len(np.unique(conv_pred)))
# print(pd.conv(true_speeds))
# print(dates)
dc.multi_fitted_line(num,conv_true,conv_pred)
dc.multi_true_v_pred(num,conv_true,conv_pred)
dc.multi_residual_plot(num,conv_true,conv_pred)