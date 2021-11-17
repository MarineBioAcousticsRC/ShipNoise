from keras.models import load_model
import data_gen_mixed_stand as pd
import numpy as np 
import ML_data_collection as dc
import model_gen as mg
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

folder = "J:\Pickled_Data_2\\"
filepath = 'J:\\scripts\\ML_Attempts\\Weights\\Mixed_Data\\attempt_2015.h5'
#definition of R^2 loss function
def coeff_determination(y_true, y_pred):
    pd.conv(y_true)
    pd.conv(y_pred)
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

#Root Mean Squared Error
def RMSE(y_true, y_pred):
    return K.sqrt(K.mean(K.square(pd.conv(y_pred) - pd.conv(y_true))))
    
#mean absolute error but in m/s so its more readable
def conv_mae(y_true, y_pred):
    return K.mean(abs(pd.conv(y_pred) - pd.conv(y_true)))
    
mlp = mg.create_mlp(5, regress=False)
cnn = mg.create_cnn(508, 508, 1, filters=(16,32), regress=False)
 
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
model.compile(loss='mae', optimizer=adam,metrics=[conv_mae,RMSE,coeff_determination])

model.load_weights(filepath)

x_data,true_speeds,dates = pd.eval_batch(folder,1000)
pred_speeds = model.predict(x_data)
pred_speeds_conv = pd.conv(pred_speeds)
print(pd.conv(true_speeds))
print(dates)

for i in range(len(dates)):
    if dates[i] == 0:
        dates.pop(i)
        true_speeds.pop(i)
        pred_speeds_conv.pop(i)
        
dc.residual_plot(2015,pd.conv(true_speeds),pred_speeds_conv,)
# dc.fitted_line(2015,pd.conv(true_speeds),pred_speeds_conv,dates)
dc.true_v_pred(2015,pd.conv(true_speeds),pred_speeds_conv)