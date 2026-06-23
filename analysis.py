import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Load dataset
df = pd.read_csv("data/HHS_Unaccompanied_Alien_Children_Program.csv")

# First 5 rows
print("========== FIRST 5 ROWS ==========")
print(df.head())

# Dataset information
print("\n========== DATASET INFO ==========")
print(df.info())

# Column names
print("\n========== COLUMNS ==========")
print(df.columns)

# Shape
print("\n========== SHAPE ==========")
print(df.shape)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# Remove completely empty rows
df = df.dropna(how='all')

print("\nAfter removing empty rows:")
print(df.shape)

df['Date'] = pd.to_datetime(df['Date'])



# Remove commas from HHS Care column
df['Children in HHS Care'] = (
    df['Children in HHS Care']
    .str.replace(',', '')
)

# Convert to numeric
df['Children in HHS Care'] = pd.to_numeric(
    df['Children in HHS Care']
)

df = df.sort_values('Date')
print(df.head())

df['Total_System_Load'] = (
    df['Children in CBP custody']
    +
    df['Children in HHS Care']
)

print(df['Total_System_Load'])

df['Net_Intake'] = (
    df['Children transferred out of CBP custody']
    -
    df['Children discharged from HHS Care']
)

print(df[['Date', 'Net_Intake']].head())

df['Backlog'] = df['Net_Intake'].cumsum()

print(df[['Date','Backlog']].head())

print("\n===== KPI SUMMARY =====")

print("Average Total Load:",
      df['Total_System_Load'].mean())

print("Maximum Total Load:",
      df['Total_System_Load'].max())

print("Minimum Total Load:",
      df['Total_System_Load'].min())

print("Average Net Intake:",
      df['Net_Intake'].mean())

# graph of system load with respect to the date
plt.figure(figsize=(12,5))

plt.plot(
    df['Date'],
    df['Total_System_Load']
)

plt.title("Total System Load Over Time")
plt.xlabel("Date")
plt.ylabel("Children Under Care")

plt.grid(True)
plt.tight_layout()

plt.show()

#graph between CBP and HSS
plt.figure(figsize=(12,5))

plt.plot(
    df['Date'],
    df['Children in CBP custody'],
    label='CBP Custody'
)

plt.plot(
    df['Date'],
    df['Children in HHS Care'],
    label='HHS Care'
)

plt.title("CBP vs HHS Load Comparison")
plt.xlabel("Date")
plt.ylabel("Number of Children")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

df['Month'] = df['Date'].dt.to_period('M')
monthly_load = (
    df.groupby('Month')
    ['Total_System_Load']
    .mean()
)

import matplotlib.pyplot as plt

#graph of the monthly avg system load
plt.figure(figsize=(14,5))

monthly_load.plot()

plt.title("Monthly Average System Load")
plt.xlabel("Month")
plt.ylabel("Average Load")

plt.grid(True)
plt.tight_layout()

plt.show()

# graph of backlog Accumulation trend between date and the backlog
plt.figure(figsize=(12,5))

plt.plot(
    df['Date'],
    df['Backlog']
)

plt.title("Backlog Accumulation Trend")
plt.xlabel("Date")
plt.ylabel("Backlog")

plt.grid(True)
plt.tight_layout()

plt.show()
# From  there our machine leaning part starts which predict the future outcomes of out project from the previous.
df['Day_Number'] = range(len(df))# convert the dates into numbers because machine leaning doesnot understand dates directly.

X = df[['Day_Number']] # train over the past data
Y = df['Total_System_Load']

model = LinearRegression() #train the model
model.fit(X, Y)

# next 30 days prediction 
future_days = np.arange(
    len(df),
    len(df) + 30
).reshape(-1,1)

future_predictions = model.predict(
    future_days
)

future_dates = pd.date_range(
    start=df['Date'].max() + pd.Timedelta(days=1),
    periods=30
)
print("\n===== NEXT 30 DAY FORECAST =====")

print(future_predictions)

# This shows the graph of prediction model.
plt.figure(figsize=(14,6))

# Historical Data
plt.plot(
    df['Date'],
    df['Total_System_Load'],
    label='Historical Data'

)

# Forecast Data
plt.plot(
    future_dates,
    future_predictions,
    label='Forecast'
)

plt.title("30-Day System Load Forecast")

plt.xlabel("Date")
plt.ylabel("Number of Children Under Care")

plt.legend()

plt.grid(True)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
