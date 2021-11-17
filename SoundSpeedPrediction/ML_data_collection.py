
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_file(file):
    with open(file, mode='w+') as file:
        file.write("attempt_num,features,epochs_run,val_mae_0,val_mae_100,val_mae_200,val_rmse_0,val_rmse_100,val_rmse_200,R^2_0,R^2_100,R^2_200,")


def write_json(file, json):
    with open(file, mode='w+') as file:
        file.write(json)


def write_data(data, file):
    with open(file, mode='a') as file:
        csv_writer = csv.writer(file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(data)


def print_data(file):
    df = pd.read_csv(file, sep='\s*,\s*')
    print(df)


def get_num(file="J:\scripts\ML_Attempts\CSV_Files\Mixed_Data_Vector_kf.csv"):
    df = pd.read_csv(file, sep='\s*,\s*')
    return (df['attempt_num'].iloc[-1]) + 1


def plot_data(num, epoch, loss, val_loss, mae, val_mae):

    destination = "J:\scripts\ML_Attempts\Generated_Plots\Mixed_Data_Vector_kf{}".format(
        num)

    epochs = range(epoch+1)

    plt.plot(epochs, loss, 'r-', label="Loss")
    plt.plot(epochs, val_loss, 'r--', label="Val_Loss")
    plt.plot(epochs, mae, 'b-', label="MAE")
    plt.plot(epochs, val_mae, 'b--', label="Val_MAE")

    plt.yscale('log')
    plt.legend()
    plt.xlabel("Epochs")
    plt.title("Mixed_Data_{}".format(num))

    plt.savefig(destination)
    plt.close()


def residual_plot(num, true, pred):
    destination = "J:\scripts\ML_Attempts\Generated_Residual_Plots\Mixed_Data_Vector_kf{}".format(
        num)
    residuals = []
    for i in range(len(true)):
        residuals.append(true[i]-pred[i])
    # print(residuals)
    plt.plot(true, residuals, 'r.', label="True Value - Predicted Value")
    # plt.axis([0, len(true), 0, 15])
    # plt.axhline(0)
    # plt.legend()
    plt.xlabel("Date")
    plt.title("Mixed_Data_{}".format(num))

    plt.savefig(destination)
    plt.close()


def multi_residual_plot(num, true, pred):
    destination = "J:\scripts\ML_Attempts\Generated_Residual_Plots\Mixed_Data_Vector_kf{}".format(
        num)

    residuals_0 = []
    residuals_100 = []
    residuals_200 = []
    myDiff = true-pred

    for i in range(200):
        print(i)
        residuals_0.append(np.sqrt(np.mean(np.square(myDiff[:,i]))))

    #for i in range(len(true[1])):
    #    residuals_100.append(true[1][i]-pred[1][i])

    #for i in range(len(true[2])):
    #    residuals_200.append(true[2][i]-pred[2][i])

    plt.title("Mixed_Data_Residual_{} (True Value - Predicted Value)".format(num))
    ax1 = plt.subplot(111)
    ax1.plot(residuals_0, 'r.',
             label="True Value - Predicted Value", alpha=0.2)
    start, end = ax1.get_ylim()
    #ax1.yaxis.set_ticks(np.arange(-10, 10, 2))
    
    # ax1.axhline(y=0)
    # plt.legend()

    #ax2 = plt.subplot(312)
    #ax2.plot(true[1], residuals_100, 'm.',
    #         label="True Value - Predicted Value", alpha=0.2)
    #start, end = ax2.get_ylim()
    #ax2.yaxis.set_ticks(np.arange(-10, 10, 2))
    #ax2.axhline(y=0)
    ## plt.legend()

    #ax3 = plt.subplot(313)
    #ax3.plot(true[2], residuals_200, 'g.',
    #         label="True Value - Predicted Value", alpha=0.2)
    #start, end = ax3.get_ylim()
    #ax3.yaxis.set_ticks(np.arange(-10, 10, 2))
    #ax3.axhline(y=0)
    ## plt.legend()

    plt.savefig(destination)
    plt.close()


def fitted_line(num, true, pred, dates):
    destination = "J:\scripts\ML_Attempts\Generated_Residual_Plots\Mixed_Data_Vector_kf{}".format(
        num)

    plt.plot(true, 'r.', label="True Values")
    plt.plot(pred, 'b-', label="Predicted Values")
    # plt.legend()
    plt.title("Mixed_Data_Fitted_Line_{}".format(num))

    plt.savefig(destination)
    plt.close()


def multi_fitted_line(num, true, pred):
    destination = "J:\scripts\ML_Attempts\Generated_Residual_Plots\Mixed_Data_fitted_line_kf{}".format(
        num)

    plt.title("Mixed_Data_Fitted_Line_{}".format(num))
    true = np.reshape(true,(1,true.size))
    pred = np.reshape(pred,(1,pred.size))
    ax1 = plt.subplot(111)
    plt.plot(true, 'r.', label="True Values: 0")
    plt.plot(pred, 'b-', label="Predicted Values: 0")
    #ax1.legend(loc='upper center', bbox_to_anchor=(
    #    0.5, -0.05), shadow=True, ncol=2)

    #ax2 = plt.subplot(312)
    #plt.plot(true[1], 'm.', label="True Values @ Depth: 100")
    #plt.plot(pred[1], 'y-', label="Predicted Values @ Depth: 100")
    #ax2.legend(loc='upper center', bbox_to_anchor=(
    #    0.5, -0.05), shadow=True, ncol=2)

    #ax3 = plt.subplot(313)
    #plt.plot(true[2], 'g.', label="True Values @ Depth: 200")
    #plt.plot(pred[2], 'c-', label="Predicted Values @ Depth: 200")
    #ax3.legend(loc='upper center', bbox_to_anchor=(
    #    0.5, -0.05), shadow=True, ncol=2)

    plt.savefig(destination)
    plt.close()


def true_v_pred(num, true, pred):
    destination = "J:\scripts\ML_Attempts\Generated_Plots\Mixed_Data_Vector_kf_{}".format(
        num)

    x_range = range(1490, 1520)
    y_range = range(1490, 1520)
    plt.plot(x_range, y_range, 'b-')
    plt.plot(true, pred, 'r.')
    plt.legend(fontsize='small')
    plt.title("Mixed_Data_True_v_Pred_{}".format(num))

    plt.savefig(destination)
    plt.close()


def multi_true_v_pred(num, true, pred):
    destination = "J:\scripts\ML_Attempts\Generated_Plots\Mixed_Data_t_v_p_{}".format(
        num)
    true = np.reshape(true,(1,true.size))
    pred = np.reshape(pred,(1,pred.size))

    x_range = range(1490, 1520)
    y_range = range(1490, 1520)
    plt.plot(x_range, y_range, 'b-')

    plt.plot(true, pred, 'r.', alpha=0.2)
    #plt.plot(true[1], pred[1], 'm.',
    #         label="Predicted Values @ Depth: 100", alpha=0.2)
    #plt.plot(true[2], pred[2], 'g.',
    #         label="Predicted Values @ Depth: 200", alpha=0.2)

    plt.legend(fontsize ='small')
    plt.title("Mixed_Data_True_v_Pred_{}".format(num))

    plt.savefig(destination)
    plt.close()
# create_file("J:\scripts\ML_Attempts\CSV_Files\Mixed_Data_Multi_Depth.csv")
# print_data("J:\scripts\ML_Attempts\CSV_Files\Mixed_Data_r2.csv")
