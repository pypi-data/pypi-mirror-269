import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

# Step 1: Generate Random Time Series Data
np.random.seed(0)
date_range = pd.date_range(start='2020-01-01', end='2023-12-31', freq='M')
values = np.random.randint(0, 100, size=len(date_range))
data = pd.DataFrame({'date': date_range, 'value': values})

# Plot the time series data
plt.figure(figsize=(10, 6))
plt.plot(data['date'], data['value'], color='blue')
plt.title('Random Time Series Data')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True)
plt.show()

# Step 2: Check for Stationarity
result = adfuller(data['value'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:')
for key, value in result[4].items():
    print(f'{key}: {value}')
if result[1] <= 0.05:
    print('Data is stationary (reject null hypothesis)')
else:
    print('Data is non-stationary (fail to reject null hypothesis)')

# Step 3: Plot Correlation and Auto-Correlation Charts
plt.figure(figsize=(10, 6))
plot_acf(data['value'], lags=20)
plt.title('Autocorrelation')
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.show()

plt.figure(figsize=(10, 6))
plot_pacf(data['value'], lags=20)
plt.title('Partial Autocorrelation')
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.show()

# Step 4: Construct ARIMA Model
# Assuming you have determined the order parameters (p, d, q) for ARIMA
p = 1
d = 1
q = 1

# Fit the ARIMA model
model = ARIMA(data['value'], order=(p, d, q))
fit_model = model.fit()

# Print model summary
print(fit_model.summary())
