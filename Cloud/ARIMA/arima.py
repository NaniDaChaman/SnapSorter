
from pandas import read_csv
from datetime import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
 
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
 

#pyplot.show()

def get_prediction(previous,n) :
    model = ARIMA(previous, order=(1, 1, 1))
    fitted_model = model.fit()
    forecast = fitted_model.forecast(steps=n)
    return forecast
    #print(forecast)

#def moving_avg(array):
      #model



def main():
    series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0,  date_parser=parser)
    print(series.head())
    #series.plot()
    print(f"forecast for next prediction : {get_prediction(series.iloc[0:3,0].to_numpy(),10)}")

if __name__ == '__main__':
      main()