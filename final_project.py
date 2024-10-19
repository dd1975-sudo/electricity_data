import os
import pandas as pd
import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# Relative path to the 'data' folder in the repository
data_folder_path = 'data'

file_to_open_electricity = 'Electricity_20-09-2024.csv'
file_to_open_price = 'sahkon-hinta-010121-240924.csv'

# Using relative paths to load the CSV files
file_path_electricity = os.path.join(data_folder_path, file_to_open_electricity)
file_path_price = os.path.join(data_folder_path, file_to_open_price)

# Loading the CSV files
columns_to_load = ['Time', 'Energy (kWh)', 'Temperature']
df_el = pd.read_csv(file_path_electricity, delimiter=';', na_values=[''], usecols=columns_to_load)
df_pr = pd.read_csv(file_path_price, na_values=[''])

# --- start: strings to floats in electricity
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].str.replace(',', '.')
df_el['Temperature'] = df_el['Temperature'].str.replace(',', '.')
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].astype(float)
df_el['Temperature'] = df_el['Temperature'].astype(float)
df_el = df_el.dropna(subset=['Energy (kWh)'])
df_el = df_el[df_el['Energy (kWh)'] != 0]

# Convert 'Time' columns to Pandas datetime
df_el['Time'] = pd.to_datetime(df_el['Time'], dayfirst=True, errors='coerce')
df_pr['Time'] = pd.to_datetime(df_pr['Time'], dayfirst=True, errors='coerce')

# Merge the two datasets on 'Time'
df_merged_data = pd.merge(df_el, df_pr, on='Time', how='inner')

# Calculate the hourly cost
df_merged_data['Cost (€)'] = df_merged_data['Energy (kWh)'] * (df_merged_data['Price (cent/kWh)'] / 100)
df_hourly_bill = df_merged_data[['Time', 'Cost (€)']]
df_hourly_bill.loc[:, 'Cost (€)'] = df_hourly_bill['Cost (€)'].round(2)

# Calculate daily, weekly, and monthly statistics
df_daily_consumption = df_merged_data.groupby(pd.Grouper(key='Time', freq='D'))['Energy (kWh)'].sum().reset_index()
df_daily_bill = df_merged_data.groupby(pd.Grouper(key='Time', freq='D'))['Cost (€)'].sum().reset_index()
df_daily_bill.loc[:, 'Cost (€)'] = df_daily_bill['Cost (€)'].round(2)
df_daily_avg_price = df_merged_data.groupby(pd.Grouper(key='Time', freq='D'))['Price (cent/kWh)'].mean().reset_index()
df_daily_avg_price.loc[:, 'Price (cent/kWh)'] = df_daily_avg_price['Price (cent/kWh)'].round(2)
df_daily_avg_temp = df_merged_data.groupby(pd.Grouper(key='Time', freq='D'))['Temperature'].mean().reset_index()

# Streamlit app starts here
st.title('Electricity Consumption and Cost Analysis')

min_date = df_merged_data['Time'].min()
max_date = df_merged_data['Time'].max()

start_date = st.date_input(
    f"Select starting date (Available data: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')})",
    value=min_date, min_value=min_date, max_value=max_date
)

end_date = st.date_input(
    f"Select ending date (Available data: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')})",
    value=max_date, min_value=min_date, max_value=max_date
)

interval = st.selectbox('Select grouping interval:', ("Daily", "Weekly", "Monthly"))

# Assign the appropriate frequency for grouping
if interval == "Daily":
    grouping_freq = "D"
elif interval == "Weekly":
    grouping_freq = "W"
elif interval == "Monthly":
    grouping_freq = "ME"

if start_date and end_date:
    df_filtered_timerange = df_merged_data[(df_merged_data['Time'] >= pd.to_datetime(start_date)) &
                                           (df_merged_data['Time'] <= pd.to_datetime(end_date))]

    st.markdown(f"### Data for the selected period ({start_date} to {end_date}):")
    consumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    bill = df_filtered_timerange['Cost (€)'].sum().round(2)
    avg_price = df_filtered_timerange['Price (cent/kWh)'].mean().round(2)
    avg_temperature = df_filtered_timerange['Temperature'].mean().round(1)

    st.markdown(f"**Total Consumption:** {consumption} kWh")
    st.markdown(f"**Total Bill:** {bill} €")
    st.markdown(f"**Average Price:** {avg_price} cent/kWh")
    st.markdown(f"**Average Temperature:** {avg_temperature} °C")

    # Line chart of the selected grouping
    df_for_chart = df_filtered_timerange.groupby(pd.Grouper(key='Time', freq=grouping_freq)).agg({
        'Energy (kWh)': 'sum',
        'Cost (€)': 'sum',
        'Price (cent/kWh)': 'mean',
        'Temperature': 'mean'
    }).reset_index()

    st.line_chart(df_for_chart, x='Time', y='Energy (kWh)', use_container_width=True)
    st.line_chart(df_for_chart, x='Time', y='Cost (€)', use_container_width=True)
