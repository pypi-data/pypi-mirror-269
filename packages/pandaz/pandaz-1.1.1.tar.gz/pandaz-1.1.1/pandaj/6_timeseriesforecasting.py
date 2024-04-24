import numpy as np
import pandas as pd
import scipy
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels import tsa


df = pd.read_csv("supermarket_sales - Sheet1.csv")
df.head()


df['Date'] = pd.to_datetime(df['Date'])
df.head(2)


data = df.loc[df['City'] == 'Yangon']
r_col = ['Invoice ID', 'Branch', 'City', 'Customer type', 'Gender',
       'Product line', 'Unit price', 'Quantity', 'Tax 5%',
       'Time', 'Payment', 'cogs', 'gross margin percentage', 'gross income',
       'Rating',]


data.drop(r_col, axis =1 , inplace=True)
data.head()


data = data[["Date","Total"]]
data = data.sort_values('Date')
data.set_index('Date', inplace=True)
data.head()
df1=data


data.plot(figsize=(15,6),legend=True)
plt.ylabel("Sales",fontsize=18)
plt.xlabel("Date",fontsize=18)
plt.title("Date Vs Sales",fontsize=20)
plt.show()


from statsmodels.tsa.stattools import adfuller

result = adfuller(data['Total'])
print('ADF Statistic: ', result[0])
print('p-value: ', result[1])


data = data['Total'].resample('D').mean()
data.head()


from statsmodels.tsa.seasonal import seasonal_decompose

decompose_result_mult = seasonal_decompose(data, model="multiplicative")

trend = decompose_result_mult.trend
seasonal = decompose_result_mult.seasonal
residual = decompose_result_mult.resid

decompose_result_mult.plot()


from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
fig = sm.graphics.tsa.plot_acf(data, lags=40)


fig = sm.graphics.tsa.plot_pacf(data, lags=40)


from sklearn.model_selection import train_test_split
inputs = df1.index
target = df1['Total'].copy()
X_train, X_test, y_train, y_test = train_test_split(inputs,target, test_size=1/3, random_state=0)


from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from math import sqrt

model = ARIMA(y_train, order=(0,3,1))
model_fit = model.fit()


predictions = model_fit.forecast(len(y_test))


mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
rmse = sqrt(mse)
print(mse)
print(mae)
print(rmse)