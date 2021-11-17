import data_gen_mixed_validation as pd
import ML_data_collection as dc
import model_gen as mg
import numpy as np
import tensorflow as tf
import unpickle as up
from custom_losses_val import (RMSE_0, RMSE_100, RMSE_200, conv_mae_0,
                               conv_mae_100, conv_mae_200,
                               euclidean_distance_loss, r_2)
from DataGenerator import Generator
from keras import backend as K
from keras import optimizers, regularizers
from keras.callbacks import EarlyStopping, PrintCallback, TensorBoard
from keras.layers import (Activation, Dense, Dropout, Flatten, Input,
                          concatenate)
from keras.models import Model, model_from_json
from keras.utils import np_utils

# setup backend and gpu
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.85
sess = tf.Session(config=config)
K.tensorflow_backend.set_session(tf.Session(config=config))
K.tensorflow_backend._get_available_gpus()

folder1 = "J:\\Pickled_Data_2\\"
folder2 = "J:\\Shipping_Validation\\New_Val\\"

num = 3030


def load_model(a_num):
    # model reconstruction from JSON:
    json_string = open(
        'J:\\scripts\\ML_Attempts\\JSON\\Mixed_Data_Vector\\attempt_{}.txt'.format(a_num), 'r').read()
    print('Loaded Model Structure')
    model = model_from_json(json_string)
    model.load_weights(
        'J:\\scripts\\ML_Attempts\\Weights\\Mixed_Data_Vector\\attempt_{}.h5'.format(a_num))
    print('Loaded Weights')
    return model


def make_prediction(x_data, true_speeds, model):
    print('Fetched Data')
    pred_speeds = model.predict(x_data)
    pred_0 = []
    pred_100 = []
    pred_200 = []

    for i in range(len(pred_speeds[0])):
        pred_0.append(pd.conv(pred_speeds[0][i][0], 0))
    for i in range(len(pred_speeds[1])):
        pred_100.append(pd.conv(pred_speeds[1][i][0], 1))
    for i in range(len(pred_speeds[2])):
        pred_200.append(pd.conv(pred_speeds[2][i][0], 2))

    raw_pred_0 = []
    raw_pred_100 = []
    raw_pred_200 = []

    for i in range(len(pred_speeds[0])):
        raw_pred_0.append(pred_speeds[0][i][0])
    for i in range(len(pred_speeds[1])):
        raw_pred_100.append(pred_speeds[1][i][0])
    for i in range(len(pred_speeds[2])):
        raw_pred_200.append(pred_speeds[2][i][0])
    raw_pred_speeds = np.array([raw_pred_0, raw_pred_100, raw_pred_200])

    # convert all speeds for plotting
    true_0 = pd.conv(true_speeds[0], 0)
    true_100 = pd.conv(true_speeds[1], 1)
    true_200 = pd.conv(true_speeds[2], 2)

    conv_true = np.array([true_0, true_100, true_200])
    conv_pred = np.array([pred_0, pred_100, pred_200])
    print("Made Predictions")
    # print(conv_true)
    # print(conv_pred)
    return raw_pred_speeds, conv_true, conv_pred


def eval_metrics(true, pred):
    print("Evaluating")
    r_2_0 = r_2(true[0], pred[0])
    r_2_100 = r_2(true[1], pred[1])
    r_2_200 = r_2(true[2], pred[2])

    rmse_0 = RMSE_0(true[0], pred[0])
    rmse_100 = RMSE_200(true[1], pred[1])
    rmse_200 = RMSE_200(true[2], pred[2])

    mae_0 = conv_mae_0(true[0], pred[0])
    mae_100 = conv_mae_100(true[1], pred[1])
    mae_200 = conv_mae_200(true[2], pred[2])

    print("""===========================================
                       Eval Results
        -------------------------------------------
                     0    |  100    |   200
        -------------------------------------------
        conv_mae: {:1.4f} | {:1.4f} | {:1.4f}
        -------------------------------------------
        RMSE:     {:1.4f} | {:1.4f} | {:1.4f}
        -------------------------------------------
        R^2:      {:1.4f} | {:1.4f} | {:1.4f}
        ===========================================\n"""
          .format(mae_0, mae_100, mae_200,
                  rmse_0, rmse_100, rmse_200,
                  r_2_0, r_2_100, r_2_200))


def clean_data(pred):
    ii = np.where(pred[0] < 1480)[0]
    return ii


def eval_model(attempt_num, folder):
    a_Model = load_model(attempt_num)
    ships, x_data, raw_true = pd.eval_batch(folder, 200)
    raw_pred, conv_true, conv_pred = make_prediction(x_data, raw_true, a_Model)
    ii = clean_data(conv_pred)
    for index in ii:
        print(ships[index].id)
        up.one_jar(folder, ships[index], True)
    eval_metrics(raw_true, raw_pred)
    dc.multi_fitted_line(5000, conv_true, conv_pred)
    dc.multi_true_v_pred(5000, conv_true, conv_pred)
    dc.multi_residual_plot(5000, conv_true, conv_pred)


eval_model(num, folder2)
