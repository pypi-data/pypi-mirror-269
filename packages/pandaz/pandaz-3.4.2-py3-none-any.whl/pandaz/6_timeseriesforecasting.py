import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA


# Load the dataset
file_path = 'california_housing_train.csv'
df = pd.read_csv(file_path)

# Prepare data for time series analysis
df['date'] = pd.date_range(start='1/1/1990', periods=len(df), freq='D')
df.set_index('date', inplace=True)

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(df['median_house_value'])
plt.title('Median House Value Over Time')
plt.xlabel('Date')
plt.ylabel('Median House Value')
plt.show()

# Decompose the time series
decomposition = seasonal_decompose(df['median_house_value'], model='additive', period=365)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plot decomposed components
decomposition.plot()
plt.show()

# Plot ACF and PACF
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(df['median_house_value'], lags=50, ax=ax[0])
plot_pacf(df['median_house_value'], lags=50, ax=ax[1])
plt.show()

# Perform Augmented Dickey-Fuller test
adf_result = adfuller(df['median_house_value'])
print('ADF Statistic:', adf_result[0])
print('p-value:', adf_result[1])
print('Critical Values:')
for key, value in adf_result[4].items():
    print(f'   {key}: {value}')

# Define forecasting functions
def linear_regression_forecast(data, window):
    X = pd.DataFrame({'t': range(1, len(data) + 1)})
    y = data.values
    model = LinearRegression()
    model.fit(X[-window:], y[-window:])
    return model.predict([[len(data) + 1]])[0]

def moving_average_forecast(data, window):
    return data.rolling(window=window).mean().iloc[-1]

def arima_forecast(data, order):
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    return model_fit.forecast()[0]

# Define window size and ARIMA order
window_size = 30
arima_order = (5, 1, 0)

# Perform forecasts
linear_regression_forecast_value = linear_regression_forecast(df['median_house_value'], window_size)
moving_average_forecast_value = moving_average_forecast(df['median_house_value'], window_size)
arima_forecast_value = arima_forecast(df['median_house_value'], order=arima_order)

# Compute evaluation metrics
actual_value = df['median_house_value'].iloc[-1]
linear_regression_mae = mean_absolute_error([actual_value], [linear_regression_forecast_value])
moving_average_mae = mean_absolute_error([actual_value], [moving_average_forecast_value])
arima_mae = mean_absolute_error([actual_value], [arima_forecast_value])

# Print evaluation metrics
print("Evaluation Metrics:")
print("Linear Regression:")
print("MAE:", linear_regression_mae)
print("Moving Average:")
print("MAE:", moving_average_mae)
print("ARIMA:")
print("MAE:", arima_mae)
