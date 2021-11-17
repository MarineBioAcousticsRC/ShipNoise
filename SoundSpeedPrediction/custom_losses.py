import data_gen_mixed_stand_vector_KF as pd
from keras import backend as K
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
# definition of R^2 loss function


def r_2(y_true, y_pred):
    """
    R^2 Value Of Model
    https://en.wikipedia.org/wiki/Coefficient_of_determination
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    SS_res = K.sum(K.square(y_true-y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    #return (1. - (SS_res/(SS_tot + K.epsilon())))
    return (SS_res/(SS_tot + K.epsilon()))

# Root Mean Squared Error


def RMSE_0(y_true, y_pred):
    """
    Standardized Root Mean Squared Error
    http://en.wikipedia.org/wiki/Root-mean-square_deviation
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    #y_true = pd.conv(y_true)
    #y_pred = pd.conv(y_pred)
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

# mean absolute error but in m/s so its more readable
def conv_mae_0(y_true, y_pred):
    """
    Unstandardized Mean Absolute Error  
    https://en.wikipedia.org/wiki/Mean_absolute_error
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    #print('true tensor shape {}'.format(K.int_shape(y_true)))
    #print('predicted tensor shape {}'.format(K.int_shape(y_pred)))
    #y_true = y_true[:,1:]-y_true[:,:-1]
    #y_pred = y_pred[:,1:]-y_pred[:,:-1]
    return K.mean(K.abs(y_pred - y_true), axis=-1)

# mean absolute error but in m/s so its more readable

def corr_0(y_true, y_pred):
    """
    Unstandardized Mean Absolute Error  
    https://en.wikipedia.org/wiki/Mean_absolute_error
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """
    #print('true tensor shape {}'.format(K.int_shape(y_true)))
    #print('predicted tensor shape {}'.format(K.int_shape(y_pred)))
    #y_true = pd.conv(y_true)
    #y_pred = pd.conv(y_pred)
    #mx = K.mean(y_pred,axis=-1)
    #my = K.mean(y_true,axis=-1)
    #print('true mean shape {}'.format(K.int_shape(my)))
    #print('predicted mean shape {}'.format(K.int_shape(mx)))
    #xm, ym = y_pred-mx, y_true-my
    
    #corrNum = K.sum(K.dot(xm,ym))
    #corrDnum = tf.multiply(tf.norm(xm,axis=-1), tf.norm(ym,axis=-1))
    #r = 1-(corrNum / corrDnum)
    x=y_true
    y=y_pred
    axis = -1
    n = tf.cast(tf.shape(x)[axis], y_true.dtype)
    m = tf.cast(tf.shape(x)[0], x.dtype)

    xsum = tf.reduce_sum(x, axis=axis)
    ysum = tf.reduce_sum(y, axis=axis)
    xmean = xsum / n
    ymean = ysum / n
    xmean = K.reshape(xmean,[m,1])
    ymean = K.reshape(ymean,[m,1])
    xsqsum = tf.reduce_sum(tf.squared_difference(x, xmean), axis=axis)
    ysqsum = tf.reduce_sum(tf.squared_difference(y, ymean), axis=axis)
    cov = tf.reduce_sum((x - xmean) * (y - ymean), axis=axis)
    corr = cov / tf.sqrt(xsqsum * ysqsum)
    #sqdif = tf.reduce_sum(tf.squared_difference(x, y), axis=axis) / n / tf.sqrt(ysqsum / n)
    # meandif = tf.abs(xmean - ymean) / tf.abs(ymean)
    # vardif = tf.abs(xvar - yvar) / yvar
    return tf.convert_to_tensor(tf.constant(1.0, dtype=x.dtype)-corr)
    # return tf.convert_to_tensor( K.mean(tf.constant(1.0, dtype=x.dtype) - corr + (0.01 * sqdif)) , dtype=tf.float32 )
    # return  tf.convert_to_tensor(K.mean(tf.constant(1.0, dtype=x.dtype)- corr), dtype=tf.float32 )


def mahal_0(y_true, y_pred):
    x=y_true
    y=y_pred
    axis = -1
    n = tf.cast(tf.shape(x)[axis], x.dtype)
    m = tf.cast(tf.shape(x)[0], x.dtype)
    xsum = tf.reduce_sum(x, axis=axis)
    ysum = tf.reduce_sum(y, axis=axis)
    xmean = xsum / n
    ymean = ysum / n
    xmean = K.reshape(xmean,[m,1])
    ymean = K.reshape(ymean,[m,1])
    xsqsum = tf.reduce_sum(tf.squared_difference(x, xmean), axis=axis)
    ysqsum = tf.reduce_sum(tf.squared_difference(y, ymean), axis=axis)
    cov = tfp.stats.covariance(xmean,ymean, axis=axis)
    x_minus_mn_with_transpose = K.transpose(x - y)
    inv_covmat = tf.linalg.inv(cov)
    x_minus_mn = x - y
    left_term = K.dot(x_minus_mn, inv_covmat)
    D_square = K.dot(left_term, x_minus_mn_with_transpose)
    return D_square

def cdist(y_true, y_pred):
    na = tf.reduce_sum(tf.square(y_true))
    nb = tf.reduce_sum(tf.square(y_pred))
    na = tf.reshape(na,[-1,1])
    nb = tf.reshape(nb,[-1,1])
    D = tf.sqrt(tf.maximum(na-2*tf.matmul(y_true,y_pred,False,True)+nb,0.0))
    return D


def mape_0(y_true, y_pred):
    # print('true tensor shape {}'.format(K.int_shape(y_true)))
    # print('predicted tensor shape {}'.format(K.int_shape(y_pred)))

    y_true = pd.conv(y_true)
    y_pred = pd.conv(y_pred)
    diff = K.abs((y_true - y_pred) / K.clip(K.abs(y_true),
                                            K.epsilon(),
                                            None))
    return 100. * K.mean(diff, axis=-1)

def tf_diff_axis_0(a):
    return a[1:]-a[:-1]
def tf_diff_axis_1(a):
    return a[:,1:]-a[:,:-1]

def euclidean_distance_loss(y_true, y_pred):
    """
    Euclidean distance loss
    https://en.wikipedia.org/wiki/Euclidean_distance
    :param y_true: TensorFlow/Theano tensor
    :param y_pred: TensorFlow/Theano tensor of the same shape as y_true
    :return: float
    """

    y_true = pd.conv(y_true)
    y_pred = pd.conv(y_pred)
    # myVec =  np.arange(1,.5,-1/400)
    # euclidDist1 = K.sqrt(K.sum(K.square((y_pred - y_true))*myVec))
    euclidDist1 = K.sqrt(K.sum(K.square(y_pred - y_true)))
    batch_size, n_elems = y_pred.get_shape()
    #y_true_diff = tf_diff_axis_1(y_true)
    #y_pred_diff = tf_diff_axis_1(y_true)
    #print(y_true_diff)
    #print(y_pred_diff)

    #euclidDist2 = K.sqrt(K.sum(K.square((y_true_diff - y_pred_diff))))
    return euclidDist1
    # return K.sqrt(K.sum(K.square(y_pred - y_true)))
