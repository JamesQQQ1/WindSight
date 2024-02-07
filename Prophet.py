import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})

# Prepare the data
data = {
    'Year': list(range(1830, 2019)),
    'TotalEnergyConsumption': [
    17999, 18488, 19037, 19558, 20120, 20769, 21384, 21937, 22572, 23225, 23931, 24970, 25836, 27037, 28188, 29549, 
    30740, 31800, 32937, 34240, 35495, 36783, 38063, 39313, 40640, 41469, 42579, 43633, 44232, 45350, 46932, 47869, 
    48885, 50416, 51633, 52855, 53932, 54858, 55900, 57101, 58330, 59730, 60899, 62417, 62940, 64485, 65154, 66065, 
    66466, 67229, 69626, 70793, 72117, 73530, 73556, 74094, 74555, 75822, 76754, 77663, 78544, 79527, 80418, 81372, 
    82306, 83278, 84222, 85130, 86179, 87071, 90238, 87858, 90645, 90202, 90088, 91304, 94274, 98642, 93564, 95077, 
    96372, 99234, 96057, 102795, 101593, 103001, 107688, 109603, 106793, 96987, 98980, 75352, 89124, 95371, 98375, 
    94405, 72961, 99430, 93272, 97946, 93627, 87336, 84167, 87189, 94005, 96996, 102238, 105715, 100577, 100240, 
    100761, 101836, 102712, 104532, 106587, 98847, 100648, 100760, 104574, 105929, 112525, 115344, 115095, 117418, 
    120927, 123065, 124374, 120268, 118821, 116644, 124802, 123426, 124869, 129683, 129342, 133125, 132470, 132333, 
    136026, 141063, 145977, 143589, 146205, 153744, 146818, 140751, 144407, 147444, 149146, 155521, 142394, 138346, 
    136726, 136111, 135753, 141867, 145719, 146132, 148569, 146180, 147268, 151818, 151091, 152747, 152548, 150384, 
    157019, 153902, 155921, 156534, 159365, 160926, 156476, 158147, 159936, 159676, 157042, 154259, 154156, 144241, 
    150496, 138587, 142330, 142989, 135609, 139372, 141310, 141103, 142724
]
}

# Convert the dictionary into a pandas DataFrame
df = pd.DataFrame(data)

# Prophet requires the columns to be named 'ds' for the date and 'y' for the value
df.rename(columns={'Year': 'ds', 'TotalEnergyConsumption': 'y'}, inplace=True)

# Convert 'ds' to DateTime format
df['ds'] = pd.to_datetime(df['ds'], format='%Y')

# Create and fit the Prophet model
model = Prophet()
model.fit(df)

# Forecasting
# Define the number of periods (years) to forecast
n_periods = 82
# Generate future dataframe
future = model.make_future_dataframe(periods=n_periods, freq='Y')

# Generate forecast results
forecast = model.predict(future)

print(forecast)

# Extract specific forecasted values for the years 2020, 2050, 2075, and 2099
forecast_2020 = forecast[forecast['ds'] == pd.to_datetime('2020-12-31')]['yhat'].values[0]
forecast_2050 = forecast[forecast['ds'] == pd.to_datetime('2050-12-31')]['yhat'].values[0]
forecast_2075 = forecast[forecast['ds'] == pd.to_datetime('2075-12-31')]['yhat'].values[0]
forecast_2099 = forecast[forecast['ds'] == pd.to_datetime('2099-12-31')]['yhat'].values[0]

# Print the extracted forecasted values
print(f"Forecast for 2020: {forecast_2020}")
print(f"Forecast for 2050: {forecast_2050}")
print(f"Forecast for 2075: {forecast_2075}")
print(f"Forecast for 2099: {forecast_2099}")

# Plotting
plt.figure(figsize=(12,6))
plt.plot(df['ds'], df['y'], label='Historical')  # Plot historical data
plt.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='red')  # Plot forecasted data
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='pink', alpha=0.3)  # Fill confidence interval
plt.title('Total UK Energy Consumption Forecast')
plt.xlabel('Year')
plt.ylabel('Total UK Energy Consumption (Thousand tonnes of oil equivalent)')
plt.legend()
plt.savefig('Population/Prophet.png')

# Forecasted energy demand data
data = {
    'Year': [2020, 2050, 2075, 2099],
    'Forecasted Demand': [153958.12613409516, 160950.34885006872, 166572.241745606, 171642.96175552055]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Calculate percentage change relative to the year 2020
baseline_2020 = df.loc['2020-01-01', 'Forecasted Demand']
df['Percentage Change from 2020'] = ((df['Forecasted Demand'] - baseline_2020) / baseline_2020) * 100

# Display the DataFrame with percentage changes
print(df)