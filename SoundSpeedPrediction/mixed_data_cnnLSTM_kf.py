
# GOAL: CONTINOUS SPEED
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation, Flatten
from keras.layers import concatenate
from keras.utils import np_utils
import model_gen as mg
from keras import optimizers
from keras import backend as K
from keras import losses
from keras.callbacks import TensorBoard, EarlyStopping, PrintCallback, BaseLogger
from keras import regularizers
import data_gen_timedistributed_KF as pd
import numpy as np
import unpickle as up
import ML_data_collection as dc
from custom_losses import corr_0,RMSE_0,r_2, conv_mae_0, mape_0, euclidean_distance_loss,cdist
# import matlab.engine
import matplotlib.pyplot as plt

# from custom_callbacks import print_callback

# Command to start TensorBoard:
# tensorboard --logdir=J:\scripts\ML_Attempts\logs\Mixed_Data_Vector_kf --host localhost --port 8088

# NUM ATTEMPT:

num = dc.get_num()
# eng = matlab.engine.start_matlab()
# ------------------------------------SETUP-------------------------------------------------------------
# set up the tensorflow backend in order to use gpu
# only give 85% of gpu over otherwise it crashes
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.85
sess = tf.Session(config=config)
K.tensorflow_backend.set_session(tf.Session(config=config))
K.tensorflow_backend._get_available_gpus()

# source folder of ships
# folder = "J:\\Pickled_Data_6\\"
# folder = "J:\\Pickled_Data_Range\\"

# create the MLP and CNN models
# model = mg.create_mlp(512, regress=True)

model = mg.create_cnn_lstm(1,20, 512, 1,1,filters=(16, 32, 64), regress=True)
#cnn = mg.create_cnn(508, 508, 1, filters=(16, 32, 64), regress=False)
#cnn = mg.create_cnn(255, 255, 1, filters=(16, 32, 64), regress=False)
# cnn = mg.create_cnn_seq(512, 512, 1, filters=(16, 32, 64), regress=True)
# create the input to our final set of layers as the *output* of both
# the MLP and CNN
# combinedInput = concatenate([mlp.output, cnn.output])

# our final FC layer head will have 4 dense layers, the final ones
# being our regression heads
#x = Dense(128, activation="relu")(combinedInput)
#x_0 = Dense(128, activation="relu")(x)

# out_0 = (Dense(200,name="Speed_0",activation="linear"))(x_0)
# out_1 = (Dense(200,name="Speed_1",activation="linear"))(out_0)

# our final model will accept categorical/numerical data on the MLP
# input and images on the CNN input, outputting a vector
# model = Model(inputs=[mlp.input, cnn.input], outputs=[out_0])
# adam is the default loss function and I see no reason to change it
# lowered learning rate to debug remember to set it back to 0.0001
adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999)

# Compile model and define all metrics different depths have different conversions therfore each
# must be converted differently unlike in the single depth model
# switched loss to euclidean_distance_loss may switch back to ['mae','mae','mae']

model.compile(loss=euclidean_distance_loss, optimizer=adam, metrics={'Speed_0': [conv_mae_0,r_2,mape_0]})

# -----------------------------------------TRAINING---------------------------------------------------------
# create callbacks one is to display realtime plots on tensorboard
# other stops training if model begins to overfit
model.summary()
#cnnlstm.run_eagerly = True

tensorboard = TensorBoard(
    log_dir='J:\\scripts\\ML_Attempts\\logs\\Mixed_Data_Vector_kf\\mixed_data_vector_kf{}'.format(num))
early_stop = EarlyStopping(
    monitor='val_loss', patience=20, restore_best_weights=True)
print_callback = PrintCallback()
# prog_callback = BaseLogger()
# remote_monitor = RemoteMonitor()
Train_Gen = pd.data_generator('train', 25)
Val_Gen = pd.data_generator('test', 5)
print('made it through data generation')
# train model using data generator in order to conserve memory
mixed = model.fit_generator(generator=Train_Gen,
                            validation_data=Val_Gen,
                            steps_per_epoch=(80), #25*100 = 7120 // 267*25=75*89=6675 
                            validation_steps=(20), #20*89 = 1780 // *9*25=2225
                            epochs=10,
                            verbose=1,
                            shuffle=False,
                            callbacks=[tensorboard, early_stop,print_callback])

# save this attempts weights after training
model.save_weights(
    'J:\\scripts\\ML_Attempts\\Weights\\Mixed_Data_Vector_kf\\attempt_{}.h5'.format(num))
json_model = model.to_json()
dc.write_json('J:\\scripts\\ML_Attempts\\JSON\\Mixed_Data_Vector_kf\\attempt_{}.txt'.format(
    num), json_model)
model.save('J:\\scripts\\ML_Attempts\\Saved_Models\\Mixed_Data_Vector_kf\\models\\1\\Ship_Noise_Mixed_Data_kf{}'.format(num))
# --------------------------------------DATA COLLECTION--------------------------------------------------------------------------

feat_array = pd.get_feats()

# this data will be saved in csv with all the other attempts
# find best epoch and use that data as that epochs weights are the ones saved.
min_in = mixed.history['val_loss'].index(min(mixed.history['val_loss']))


csv_data = [num,
            feat_array,
            early_stop.stopped_epoch,
            mixed.history['val_conv_mae_0'][min_in],

            mixed.history['val_mape_0'][min_in],
            
            mixed.history['val_r_2'][min_in]]

dc.write_data(
    csv_data, "J:\\scripts\\ML_Attempts\\CSV_Files\\Mixed_Data_Vector_kf.csv")

# this data will be plotted and the graphs will be saved
# dc.plot_data(num,
# early_stop.stopped_epoch,
# mixed.history['loss'],
# mixed.history['val_loss'],
# np.asarray(mixed.history['mean_absolute_error'])*conv,
# np.asarray(mixed.history['val_mean_absolute_error'])*conv)

# predict data and generate residual plot

x_data, true_speeds = pd.eval_batch(10)
pred_speeds = model.predict(x_data)
# print(true_speeds)
plt.plot(np.transpose(true_speeds))
pred_0 = []
destination1 = "J:\scripts\ML_Attempts\Generated_Plots\Mixed_Data_test_true_kf{}".format(
        num)
plt.savefig(destination1)
plt.close()

plt.plot(np.transpose(pred_speeds))
destination2 = "J:\scripts\ML_Attempts\Generated_Plots\Mixed_Data_test_pred_kf{}".format(
        num)
plt.savefig(destination2)
plt.close()
# print(pred_speeds)

#for i in range(len(pred_speeds[0])):
#    pred_0.append(pd.conv(pred_speeds[0][i]))
#for i in range(len(pred_speeds[2])):
#    pred_100.append(pd.conv(pred_speeds[2][i][0], 2))
#for i in range(len(pred_speeds[3])):
#    pred_200.append(pd.conv(pred_speeds[3][i][0], 3))
pred_0= pd.conv(pred_speeds)
# convert all speeds for plotting
true_0 = pd.conv(true_speeds)
#true_100 = pd.conv(true_speeds[2], 2)
#true_200 = pd.conv(true_speeds[3], 3)
# print(true_0)
np.savetxt("J:\\scripts\\ML_Attempts\\CSV_Files\\trueSpeeds_{}.csv".format(num), true_0, delimiter=",")
np.savetxt("J:\\scripts\\ML_Attempts\\CSV_Files\\predSpeeds_{}.csv".format(num), pred_0, delimiter=",")

conv_true = true_0
conv_pred = pred_0
# print(conv_true)
# print(len(np.unique(conv_true)))
# print(conv_pred)
# print(len(np.unique(conv_pred)))
# print(pd.conv(true_speeds))
# print(dates)
dc.multi_fitted_line(num, conv_true, conv_pred)
dc.multi_true_v_pred(num, conv_true, conv_pred)
dc.multi_residual_plot(num, conv_true, conv_pred)


