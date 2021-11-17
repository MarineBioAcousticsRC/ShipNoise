import tensorflow as tf

class print_callback(Callback):

  def on_train_batch_end(self, batch, logs=None):
        print("""\rbatch {}: 
            mae: {:1.4f}, 
            speeds_mae: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_conv_mae: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_RMSE: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_R^2: [{:1.4f},{:1.4f},{:1.4f}]"""
            .format(epoch, 
            logs['loss'],
            logs['Speed_0_loss'],logs['Speed_100_loss'],logs['Speed_200_loss'],
            logs['Speed_0_conv_mae'],logs['Speed_100_conv_mae'],logs['Speed_200_conv_mae'],
            logs['Speed_0_RMSE'],logs['Speed_100_RMSE'],logs['Speed_200_RMSE'],
            logs['Speed_0_r_2'],logs['Speed_100_r_2'],logs['Speed_200_r_2'],))

  # def on_test_end(self, batch, logs=None):
    # print('For batch {}, loss is {:1.4f}.'.format(batch, logs['loss']))

  def on_epoch_end(self, epoch, logs=None):
    print("""epoch {}: 
            mae: {:1.4f}, 
            speeds_mae: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_conv_mae: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_RMSE: [{:1.4f},{:1.4f},{:1.4f}], 
            speeds_R^2: [{:1.4f},{:1.4f},{:1.4f}]\n"""
            .format(epoch, 
            logs['loss'],
            logs['Speed_0_loss'],logs['Speed_100_loss'],logs['Speed_200_loss'],
            logs['Speed_0_conv_mae_0'],logs['Speed_100_conv_mae_100'],logs['Speed_200_conv_mae_200'],
            logs['Speed_0_RMSE_0'],logs['Speed_100_RMSE_100'],logs['Speed_200_RMSE_200'],
            logs['Speed_0_r_2'],logs['Speed_100_r_2'],logs['Speed_200_r_2'],))
