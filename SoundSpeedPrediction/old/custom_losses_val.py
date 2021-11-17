import data_gen_mixed_validation as pd
from keras import backend as K
import numpy as np
#definition of R^2 loss function
def r_2(y_true, y_pred):
    """
    R^2 Value Of Model
    https://en.wikipedia.org/wiki/Coefficient_of_determination
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    SS_res =  np.sum(np.square(y_true-y_pred)) 
    SS_tot = np.sum(np.square(y_true - np.mean(y_true))) 
    return (1 - SS_res/(SS_tot + np.finfo(float).eps))

#Root Mean Squared Error
def RMSE_0(y_true, y_pred):
    """
    Standardized Root Mean Squared Error
    http://en.wikipedia.org/wiki/Root-mean-square_deviation
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,0)
    y_pred = pd.conv(y_pred,0)
    return np.sqrt(np.mean(np.square(y_pred - y_true)))
    
#Root Mean Squared Error
def RMSE_100(y_true, y_pred):
    """
    Standardized Root Mean Squared Error
    http://en.wikipedia.org/wiki/Root-mean-square_deviation
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,1)
    y_pred = pd.conv(y_pred,1)
    return np.sqrt(np.mean(np.square(y_pred - y_true)))

#Root Mean Squared Error
def RMSE_200(y_true, y_pred):
    """
    Standardized Root Mean Squared Error
    http://en.wikipedia.org/wiki/Root-mean-square_deviation
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,2)
    y_pred = pd.conv(y_pred,2)
    return np.sqrt(np.mean(np.square(y_pred - y_true)))    
    

#mean absolute error but in m/s so its more readable
def conv_mae_0(y_true, y_pred):
    """
    Unstandardized Mean Absolute Error  
    https://en.wikipedia.org/wiki/Mean_absolute_error
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,0)
    y_pred = pd.conv(y_pred,0)
    return np.mean(abs(y_pred - y_true))
    
#mean absolute error but in m/s so its more readable
def conv_mae_100(y_true, y_pred):
    """
    Unstandardized Mean Absolute Error  
    https://en.wikipedia.org/wiki/Mean_absolute_error
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,1)
    y_pred = pd.conv(y_pred,1)
    return np.mean(abs(y_pred - y_true))

#mean absolute error but in m/s so its more readable
def conv_mae_200(y_true, y_pred):
    """
    Unstandardized Mean Absolute Error  
    https://en.wikipedia.org/wiki/Mean_absolute_error
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    y_true = pd.conv(y_true,2)
    y_pred = pd.conv(y_pred,2)
    return np.mean(abs(y_pred - y_true))    

def euclidean_distance_loss(y_true, y_pred):
    """
    Euclidean distance loss
    https://en.wikipedia.org/wiki/Euclidean_distance
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    return np.sqrt(np.sum(np.square(y_pred - y_true), axis=-1))