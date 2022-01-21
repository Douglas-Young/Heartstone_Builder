# example of increase in mean squared error
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error

def MSE_Function(predicted_y, actual_y):
    mse_values = mean_squared_error(actual_y, predicted_y)
    mse_values = mse_values.tolist()
    pyplot.plot(mse_values)
    pyplot.xticks(ticks=[i for i in range(len(mse_values))], labels=predicted_y)
    pyplot.xlabel('Predicted Value')
    pyplot.ylabel('Mean Squared Error')
    pyplot.show()
    #print(mse_values)

    return 0
