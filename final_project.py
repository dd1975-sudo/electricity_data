<<<<<<< HEAD
# Data file Electricity_20-09-2024.csv contains information about
# hourly electricity consumption (column Energy (kWh)) and Temperature.
# Another file sahkon-hinta-010121-240924.csv contains information about
# hourly electricity prices. 

import os
import pandas as pd
import streamlit as st
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Get the current working directory and so on...
path = os.getcwd()
data_folder_path = os.path.join(path, 'final_project\\data')

file_to_open_electricity = 'Electricity_20-09-2024.csv'
file_to_open_price = 'sahkon-hinta-010121-240924.csv'

file_path_electricity = os.path.join(data_folder_path,file_to_open_electricity)
file_path_price = os.path.join(data_folder_path, file_to_open_price)

# - replace missing values with Nan
# - Specify the columns you want to load by name from electricity
columns_to_load = ['Time', 'Energy (kWh)', 'Temperature']

df_el = pd.read_csv(file_path_electricity, delimiter= ';', na_values= [''], usecols= columns_to_load)
df_pr = pd.read_csv(file_path_price, na_values= [''])

# --- start: strings to floats in electricity
# Step 1: Replace commas with dots
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].str.replace(',', '.')
df_el['Temperature'] = df_el['Temperature'].str.replace(',', '.')

# Step 2: Convert the columns to float
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].astype(float)
df_el['Temperature'] = df_el['Temperature'].astype(float)

# - Remove rows where 'Energy (kWh)' is NaN (missing)
df_el = df_el.dropna(subset=['Energy (kWh)'])

# - Remove rows where 'Energy (kWh)' is equal to 0
df_el = df_el[df_el['Energy (kWh)'] != 0]
# print(df_el)

# print(df_el)
# print('aaaaaaaaaaaaaaaaaaaaaa-------------')

# print(df_el)
# print('aaaaaaaaaaaaaaaaaaaaaa-------------')

# Display the updated DataFrame
# print(df_el)
# --- end: strings to floats

# WRONG! Format price values with a comma as the decimal separator
# df_pr['Price (cent/kWh)'] = df_pr['Price (cent/kWh)'].apply(lambda x: f'{x:.3f}'.replace('.', ','))
#print(type(df_pr['Price (cent/kWh)'][2]))

######################################################################3333
# FIRST COMPLETE THE FOLLOWING TASKS:

# ----------------------------
# 1) Start: Change time format of both files to Pandas datetime

# ---- df_el ----:
# print('Type of df_el time column values in the beginning :', type(df_el['Time'][2])) # string
# df_el = pd.to_datetime(df_el['Time'], format = '%d.%m.%Y %H:%M') # gives error

# Assuming df_el['Time'] contains your datetime strings
df_el['Time'] = pd.to_datetime(df_el['Time'], dayfirst=True, errors='coerce')
# The 'errors="coerce"' option will convert invalid date formats into NaT (Not a Time) values instead of throwing an error
# print('Type of df_el time column values in the end :', type(df_el['Time'][2])) # timestamp

# ---- df_pr ----:
# print('Type of df_pr time column values in the beginning :', type(df_pr['Time'][2])) # string
# df_pr = pd.to_datetime(df_pr['Time'], format = '%d.%m.%Y %H:%M') # gives error

# Assuming df_pr['Time'] contains your datetime strings
df_pr['Time'] = pd.to_datetime(df_pr['Time'], dayfirst=True, errors='coerce')
# The 'errors="coerce"' option will convert invalid date formats into NaT (Not a Time) values instead of throwing an error
# print('Type of df_pr time column values in the end :', type(df_pr['Time'][2])) # timestamp

# 1) End: Change time format of both files to Pandas datetime
# ----------------------------


# ----------------------------
# 2) Start: Join the two data frames according to time
# print(type(df_pr['Price (cent/kWh)'][3]))
# print(df_pr)

# a) left join => data for all dates => price for some dates / hours is missing.
# can get those values from internet later
# df_merged_left = pd.merge(df_el, df_pr, on= 'Time', how= 'left')
# print('\n Merged - left join:')
# print(df_merged_left)

# b) inner join => only dates where all data available => some dates / hours missing
df_merged_inner = pd.merge(df_el, df_pr, on= 'Time', how= 'inner')
#print('\n Merged - inner join:')
#print(df_merged_inner)

# create a df to use the selectec merging type later in in the script
df_merged_data = df_merged_inner

# 2) End: Join the two data frames according to time
# ----------------------------



# ----------------------------
# 3) Start: Calculate the hourly bill paid (using information about the price and the consumption)
df_merged_data['Cost (€)'] = df_merged_data['Energy (kWh)'] * (df_merged_data['Price (cent/kWh)'] / 100)
# print(f'\n ---- Merged data: {df_merged_data.head()}\n')

df_hourly_bill = df_merged_data[['Time','Cost (€)']]

# Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_hourly_bill.loc[:, 'Cost (€)'] = df_hourly_bill['Cost (€)'].round(2)

# print(df_hourly_bill.head(24))

# df_hourly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'h'))
# print('\n Hourly bill :')
# print(df_hourly_bill.head())

# 3) End: Calculate the hourly bill paid
# ----------------------------



# ----------------------------
# 4) Start: Calculated grouped values of daily, weekly or monthly:
#   consumption
#   bill
#   average price
#   average temperature

# Start: daily --------------------------------------------------------
# daily consumption
df_daily_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Energy (kWh)'].sum().reset_index()
# print(df_daily_consumption)

# daily bill
df_daily_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_daily_bill.loc[:, 'Cost (€)'] = df_daily_bill['Cost (€)'].round(2)
# print(df_daily_bill)

# daily average price
df_daily_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Price (cent/kWh)'].mean().reset_index()
#print(df_daily_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_daily_avg_price.loc[:, 'Price (cent/kWh)'] = df_daily_avg_price['Price (cent/kWh)'].round(2)
#print(df_daily_avg_price)

# daily average temperature
df_daily_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Temperature'].mean().reset_index()
# print(df_daily_avg_temp)
# End: daily --------------------------------------------------------

# Start: weekly --------------------------------------------------------
# weekly consumption
df_weekly_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Energy (kWh)'].sum().reset_index()
# print(df_weekly_consumption)

# weekly bill
df_weekly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_weekly_bill.loc[:, 'Cost (€)'] = df_weekly_bill['Cost (€)'].round(2)
# print(df_weekly_bill)

# weekly average price
df_weekly_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Price (cent/kWh)'].mean().reset_index()
#print(df_weekly_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_weekly_avg_price.loc[:, 'Price (cent/kWh)'] = df_weekly_avg_price['Price (cent/kWh)'].round(2)
#print(df_weekly_avg_price)

# weekly average temperature
df_weekly_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Temperature'].mean().reset_index()
# print(df_weekly_avg_temp)
# End: weekly --------------------------------------------------------


# Start: monthly --------------------------------------------------------
# monthly consumption
df_monthly_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Energy (kWh)'].sum().reset_index()
# print(df_monthly_consumption)

# monthly bill
df_monthly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_monthly_bill.loc[:, 'Cost (€)'] = df_monthly_bill['Cost (€)'].round(2)
# print(df_monthly_bill)

# monthly average price
df_monthly_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Price (cent/kWh)'].mean().reset_index()
#print(df_monthly_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_monthly_avg_price.loc[:, 'Price (cent/kWh)'] = df_monthly_avg_price['Price (cent/kWh)'].round(2)
#print(df_monthly_avg_price)

# monthly average temperature
df_monthly_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Temperature'].mean().reset_index()
# print(df_monthly_avg_temp)
# End: monthly --------------------------------------------------------

# 4) End: Calculated grouped values
# ----------------------------

############################################################################
# CREATE A VISUALIZATION WHICH INCLUDES:

# a) --- A selector for time interval included in the analysis

min_date = df_merged_data['Time'].min()
# print(f'\n Min date : {min_date}\n')

max_date = df_merged_data['Time'].max()
# print(f'\n Max date : {max_date}\n')

# Set up the date range picker for start and end dates
start_date = st.date_input(
    f"Select starting date (Data available from: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}",
    # value=[max_date - relativedelta(months = 1)],
    value=None,
    min_value=min_date,
    max_value=max_date
)

end_date = st.date_input(
    f'Select ending date (Data available from: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}',
    value=None,
    min_value=min_date,
    max_value=max_date
)

# c) --- Selector for grouping interval
interval = st.selectbox(
    'Select grouping interval:',
    ("(daily | weekly | monthly)","Daily", "Weekly", "Monthly"),
) 
# st.write(f'---INTERVAL---: {interval}')

# Assign the appropriate frequency for grouping based on the selected interval
if interval == "Daily":
    grouping_freq = "D"   # Daily
elif interval == "Weekly":
    grouping_freq = "W"   # Weekly
elif interval == "Monthly":
    grouping_freq = "ME"   # Monthly End
elif interval == "(daily | weekly | monthly)":
    grouping_freq = ""    
# st.write(grouping_freq)

# Convert selected dates to datetime for filtering
#start_date_datetime = pd.to_datetime(start_date).date()  # Convert to date
#end_date_datetime = pd.to_datetime(end_date).date()  # Convert to date

# Display the selected dates
st.write(f'Showing range: {start_date} - {end_date}')

# create a df for selected timerange (only if both dates selected)
#   Filter the grouped data based on the selected date range
if start_date is not None and end_date is not None :

    # df_filtered_timerange = df_daily_consumption[(df_daily_consumption['Time'] >= start_date_datetime) & (df_daily_consumption['Time'] <= end_date_datetime)]
    # st.write(df_merged_data.head(24))

    df_filtered_timerange = df_merged_data[(df_merged_data['Time'].dt.date >= start_date) & (df_merged_data['Time'].dt.date <= end_date)]
    # st.write(df_filtered_timerange.head(24))
    
    # b) Over selected period: ----------------------------------------
    st.markdown(f"##### &nbsp;Data for the selected period:")

    #   Consumption
    comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Total consumption: {comsumption} kWh')

    #   bill
    bill = df_filtered_timerange['Cost (€)'].sum().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Total bill: {bill} €')

    #   average price
    avg_price = df_filtered_timerange['Price (cent/kWh)'].mean().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Average price: {avg_price} cent / kWh')

    #   min price
    min_price = df_filtered_timerange['Price (cent/kWh)'].min().round(2)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Min. price: {min_price} cent / kWh')

    #   max price
    max_price = df_filtered_timerange['Price (cent/kWh)'].max().round(2)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max. price: {max_price} cent / kWh')    

    #   average temperature 
    avg_temperature = df_filtered_timerange['Temperature'].mean().round(1)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Average temperature: {avg_temperature} °C')

    #   mix temperature 
    min_temperature = df_filtered_timerange['Temperature'].min().round(1)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Min. temperature: {min_temperature} °C')

    #   max temperature 
    max_temperature = df_filtered_timerange['Temperature'].max().round(1)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max. temperature: {max_temperature} °C')        



 
# d) --- Line graphs over the range selected using the grouping interval selected. 

# plot only if dates and interval selected
if start_date is not None and end_date is not None and grouping_freq != "":

    # Dictionary to map the function name to the actual method
    agg_funcs = {
        'sum': 'sum',
        'min': 'min',
        'max': 'max',
        'mean': 'mean'
    }

    # Define the column, aggregation function, and labels
    # For single charts:
    dict_of_df = {
        'df_consumption': {
            'grouper_column': 'Energy (kWh)',
            'grouper_func': 'sum',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Electricity consumption (kWh)'
        },
        'df_cost': {
            'grouper_column': 'Cost (€)',
            'grouper_func': 'sum',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Total cost (€)'
        },
        'df_price': {
            'grouper_column': 'Price (cent/kWh)',
            'grouper_func': 'mean',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Average price of electricity (cent/kWh)'
        },
        'df_temperature': {
            'grouper_column': 'Temperature',
            'grouper_func': 'mean',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Average temperature (°C)'
        }
    }

    # Iterate over the dictionary to generate multiple charts
    for df_key, chart_info in dict_of_df.items():
        # Extract variables from the dictionary
        grouper_column = chart_info['grouper_column']
        grouper_func = chart_info['grouper_func']
        chart_label_y = chart_info['chart_label_y']
        
        # Common chart settings
        grouper_key = 'Time'
        chart_x = grouper_key
        chart_label_x = f'Time ({interval}-values)'
        chart_y = grouper_column

        # Ensure the function is valid, and apply the selected aggregation
        if grouper_func in agg_funcs:
            # Perform the grouping and aggregation
            df_for_chart = df_filtered_timerange.groupby(pd.Grouper(key=grouper_key, freq=grouping_freq))[grouper_column].agg(agg_funcs[grouper_func]).reset_index()
            
            # Plot the line chart
            st.line_chart(df_for_chart, x=chart_x, y=chart_y, x_label = chart_label_x, y_label= chart_label_y)
        else:
            st.write(f"Invalid aggregation function selected for {df_key}")

    # # column testing
    # # Create columns
    # col1, col2, col3 = st.columns(3)

    # # Display the total consumption, bill, and average price in the first column
    # with col1:
    #     st.markdown("### Data for the selected period:")
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    #     #st.write(f"**Total bill:** {total_bill:.2f} €")
    #     #st.write(f"**Average price:** {avg_price:.2f} cent / kWh")

    # # Display the min and max price in the second column
    # with col2:
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)

    # # Display the temperature data in the third column
    # with col3:
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    
=======
# Data file Electricity_20-09-2024.csv contains information about
# hourly electricity consumption (column Energy (kWh)) and Temperature.
# Another file sahkon-hinta-010121-240924.csv contains information about
# hourly electricity prices. 

import os
import pandas as pd
import streamlit as st
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Get the current working directory and so on...
path = os.getcwd()
data_folder_path = os.path.join(path, 'final_project\\data')

file_to_open_electricity = 'Electricity_20-09-2024.csv'
file_to_open_price = 'sahkon-hinta-010121-240924.csv'

file_path_electricity = os.path.join(data_folder_path,file_to_open_electricity)
file_path_price = os.path.join(data_folder_path, file_to_open_price)

# - replace missing values with Nan
# - Specify the columns you want to load by name from electricity
columns_to_load = ['Time', 'Energy (kWh)', 'Temperature']

df_el = pd.read_csv(file_path_electricity, delimiter= ';', na_values= [''], usecols= columns_to_load)
df_pr = pd.read_csv(file_path_price, na_values= [''])

# --- start: strings to floats in electricity
# Step 1: Replace commas with dots
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].str.replace(',', '.')
df_el['Temperature'] = df_el['Temperature'].str.replace(',', '.')

# Step 2: Convert the columns to float
df_el['Energy (kWh)'] = df_el['Energy (kWh)'].astype(float)
df_el['Temperature'] = df_el['Temperature'].astype(float)

# - Remove rows where 'Energy (kWh)' is NaN (missing)
df_el = df_el.dropna(subset=['Energy (kWh)'])

# - Remove rows where 'Energy (kWh)' is equal to 0
df_el = df_el[df_el['Energy (kWh)'] != 0]
# print(df_el)

# print(df_el)
# print('aaaaaaaaaaaaaaaaaaaaaa-------------')

# print(df_el)
# print('aaaaaaaaaaaaaaaaaaaaaa-------------')

# Display the updated DataFrame
# print(df_el)
# --- end: strings to floats

# WRONG! Format price values with a comma as the decimal separator
# df_pr['Price (cent/kWh)'] = df_pr['Price (cent/kWh)'].apply(lambda x: f'{x:.3f}'.replace('.', ','))
#print(type(df_pr['Price (cent/kWh)'][2]))

######################################################################3333
# FIRST COMPLETE THE FOLLOWING TASKS:

# ----------------------------
# 1) Start: Change time format of both files to Pandas datetime

# ---- df_el ----:
# print('Type of df_el time column values in the beginning :', type(df_el['Time'][2])) # string
# df_el = pd.to_datetime(df_el['Time'], format = '%d.%m.%Y %H:%M') # gives error

# Assuming df_el['Time'] contains your datetime strings
df_el['Time'] = pd.to_datetime(df_el['Time'], dayfirst=True, errors='coerce')
# The 'errors="coerce"' option will convert invalid date formats into NaT (Not a Time) values instead of throwing an error
# print('Type of df_el time column values in the end :', type(df_el['Time'][2])) # timestamp

# ---- df_pr ----:
# print('Type of df_pr time column values in the beginning :', type(df_pr['Time'][2])) # string
# df_pr = pd.to_datetime(df_pr['Time'], format = '%d.%m.%Y %H:%M') # gives error

# Assuming df_pr['Time'] contains your datetime strings
df_pr['Time'] = pd.to_datetime(df_pr['Time'], dayfirst=True, errors='coerce')
# The 'errors="coerce"' option will convert invalid date formats into NaT (Not a Time) values instead of throwing an error
# print('Type of df_pr time column values in the end :', type(df_pr['Time'][2])) # timestamp

# 1) End: Change time format of both files to Pandas datetime
# ----------------------------


# ----------------------------
# 2) Start: Join the two data frames according to time
# print(type(df_pr['Price (cent/kWh)'][3]))
# print(df_pr)

# a) left join => data for all dates => price for some dates / hours is missing.
# can get those values from internet later
# df_merged_left = pd.merge(df_el, df_pr, on= 'Time', how= 'left')
# print('\n Merged - left join:')
# print(df_merged_left)

# b) inner join => only dates where all data available => some dates / hours missing
df_merged_inner = pd.merge(df_el, df_pr, on= 'Time', how= 'inner')
#print('\n Merged - inner join:')
#print(df_merged_inner)

# create a df to use the selectec merging type later in in the script
df_merged_data = df_merged_inner

# 2) End: Join the two data frames according to time
# ----------------------------



# ----------------------------
# 3) Start: Calculate the hourly bill paid (using information about the price and the consumption)
df_merged_data['Cost (€)'] = df_merged_data['Energy (kWh)'] * (df_merged_data['Price (cent/kWh)'] / 100)
# print(f'\n ---- Merged data: {df_merged_data.head()}\n')

df_hourly_bill = df_merged_data[['Time','Cost (€)']]

# Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_hourly_bill.loc[:, 'Cost (€)'] = df_hourly_bill['Cost (€)'].round(2)

# print(df_hourly_bill.head(24))

# df_hourly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'h'))
# print('\n Hourly bill :')
# print(df_hourly_bill.head())

# 3) End: Calculate the hourly bill paid
# ----------------------------



# ----------------------------
# 4) Start: Calculated grouped values of daily, weekly or monthly:
#   consumption
#   bill
#   average price
#   average temperature

# Start: daily --------------------------------------------------------
# daily consumption
df_daily_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Energy (kWh)'].sum().reset_index()
# print(df_daily_consumption)

# daily bill
df_daily_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_daily_bill.loc[:, 'Cost (€)'] = df_daily_bill['Cost (€)'].round(2)
# print(df_daily_bill)

# daily average price
df_daily_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Price (cent/kWh)'].mean().reset_index()
#print(df_daily_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_daily_avg_price.loc[:, 'Price (cent/kWh)'] = df_daily_avg_price['Price (cent/kWh)'].round(2)
#print(df_daily_avg_price)

# daily average temperature
df_daily_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'D'))['Temperature'].mean().reset_index()
# print(df_daily_avg_temp)
# End: daily --------------------------------------------------------

# Start: weekly --------------------------------------------------------
# weekly consumption
df_weekly_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Energy (kWh)'].sum().reset_index()
# print(df_weekly_consumption)

# weekly bill
df_weekly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_weekly_bill.loc[:, 'Cost (€)'] = df_weekly_bill['Cost (€)'].round(2)
# print(df_weekly_bill)

# weekly average price
df_weekly_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Price (cent/kWh)'].mean().reset_index()
#print(df_weekly_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_weekly_avg_price.loc[:, 'Price (cent/kWh)'] = df_weekly_avg_price['Price (cent/kWh)'].round(2)
#print(df_weekly_avg_price)

# weekly average temperature
df_weekly_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'W'))['Temperature'].mean().reset_index()
# print(df_weekly_avg_temp)
# End: weekly --------------------------------------------------------


# Start: monthly --------------------------------------------------------
# monthly consumption
df_monthly_consumption = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Energy (kWh)'].sum().reset_index()
# print(df_monthly_consumption)

# monthly bill
df_monthly_bill = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Cost (€)'].sum().reset_index()

# - Safely round the 'Cost (€)' column to 2 decimal places using .loc[]
df_monthly_bill.loc[:, 'Cost (€)'] = df_monthly_bill['Cost (€)'].round(2)
# print(df_monthly_bill)

# monthly average price
df_monthly_avg_price = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Price (cent/kWh)'].mean().reset_index()
#print(df_monthly_avg_price)

# - Safely round the 'Price (cent/kWh)' column to 2 decimal places using .loc[]
df_monthly_avg_price.loc[:, 'Price (cent/kWh)'] = df_monthly_avg_price['Price (cent/kWh)'].round(2)
#print(df_monthly_avg_price)

# monthly average temperature
df_monthly_avg_temp = df_merged_data.groupby(pd.Grouper(key= 'Time', freq= 'ME'))['Temperature'].mean().reset_index()
# print(df_monthly_avg_temp)
# End: monthly --------------------------------------------------------

# 4) End: Calculated grouped values
# ----------------------------

############################################################################
# CREATE A VISUALIZATION WHICH INCLUDES:

# a) --- A selector for time interval included in the analysis

min_date = df_merged_data['Time'].min()
# print(f'\n Min date : {min_date}\n')

max_date = df_merged_data['Time'].max()
# print(f'\n Max date : {max_date}\n')

# Set up the date range picker for start and end dates
start_date = st.date_input(
    f"Select starting date (Data available from: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}",
    # value=[max_date - relativedelta(months = 1)],
    value=None,
    min_value=min_date,
    max_value=max_date
)

end_date = st.date_input(
    f'Select ending date (Data available from: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}',
    value=None,
    min_value=min_date,
    max_value=max_date
)

# c) --- Selector for grouping interval
interval = st.selectbox(
    'Select grouping interval:',
    ("(daily | weekly | monthly)","Daily", "Weekly", "Monthly"),
) 
# st.write(f'---INTERVAL---: {interval}')

# Assign the appropriate frequency for grouping based on the selected interval
if interval == "Daily":
    grouping_freq = "D"   # Daily
elif interval == "Weekly":
    grouping_freq = "W"   # Weekly
elif interval == "Monthly":
    grouping_freq = "ME"   # Monthly End
elif interval == "(daily | weekly | monthly)":
    grouping_freq = ""    
# st.write(grouping_freq)

# Convert selected dates to datetime for filtering
#start_date_datetime = pd.to_datetime(start_date).date()  # Convert to date
#end_date_datetime = pd.to_datetime(end_date).date()  # Convert to date

# Display the selected dates
st.write(f'Showing range: {start_date} - {end_date}')

# create a df for selected timerange (only if both dates selected)
#   Filter the grouped data based on the selected date range
if start_date is not None and end_date is not None :

    # df_filtered_timerange = df_daily_consumption[(df_daily_consumption['Time'] >= start_date_datetime) & (df_daily_consumption['Time'] <= end_date_datetime)]
    # st.write(df_merged_data.head(24))

    df_filtered_timerange = df_merged_data[(df_merged_data['Time'].dt.date >= start_date) & (df_merged_data['Time'].dt.date <= end_date)]
    # st.write(df_filtered_timerange.head(24))
    
    # b) Over selected period: ----------------------------------------
    st.markdown(f"##### &nbsp;Data for the selected period:")

    #   Consumption
    comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Total consumption: {comsumption} kWh')

    #   bill
    bill = df_filtered_timerange['Cost (€)'].sum().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Total bill: {bill} €')

    #   average price
    avg_price = df_filtered_timerange['Price (cent/kWh)'].mean().round(2)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Average price: {avg_price} cent / kWh')

    #   min price
    min_price = df_filtered_timerange['Price (cent/kWh)'].min().round(2)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Min. price: {min_price} cent / kWh')

    #   max price
    max_price = df_filtered_timerange['Price (cent/kWh)'].max().round(2)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max. price: {max_price} cent / kWh')    

    #   average temperature 
    avg_temperature = df_filtered_timerange['Temperature'].mean().round(1)
    st.markdown(f'###### &nbsp;&nbsp;&nbsp;Average temperature: {avg_temperature} °C')

    #   mix temperature 
    min_temperature = df_filtered_timerange['Temperature'].min().round(1)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Min. temperature: {min_temperature} °C')

    #   max temperature 
    max_temperature = df_filtered_timerange['Temperature'].max().round(1)
    st.write(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Max. temperature: {max_temperature} °C')        



 
# d) --- Line graphs over the range selected using the grouping interval selected. 

# plot only if dates and interval selected
if start_date is not None and end_date is not None and grouping_freq != "":

    # Dictionary to map the function name to the actual method
    agg_funcs = {
        'sum': 'sum',
        'min': 'min',
        'max': 'max',
        'mean': 'mean'
    }

    # Define the column, aggregation function, and labels
    # For single charts:
    dict_of_df = {
        'df_consumption': {
            'grouper_column': 'Energy (kWh)',
            'grouper_func': 'sum',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Electricity consumption (kWh)'
        },
        'df_cost': {
            'grouper_column': 'Cost (€)',
            'grouper_func': 'sum',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Total cost (€)'
        },
        'df_price': {
            'grouper_column': 'Price (cent/kWh)',
            'grouper_func': 'mean',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Average price of electricity (cent/kWh)'
        },
        'df_temperature': {
            'grouper_column': 'Temperature',
            'grouper_func': 'mean',  # This could be 'sum', 'min', 'max', or 'mean'
            'chart_label_y': 'Average temperature (°C)'
        }
    }

    # Iterate over the dictionary to generate multiple charts
    for df_key, chart_info in dict_of_df.items():
        # Extract variables from the dictionary
        grouper_column = chart_info['grouper_column']
        grouper_func = chart_info['grouper_func']
        chart_label_y = chart_info['chart_label_y']
        
        # Common chart settings
        grouper_key = 'Time'
        chart_x = grouper_key
        chart_label_x = f'Time ({interval}-values)'
        chart_y = grouper_column

        # Ensure the function is valid, and apply the selected aggregation
        if grouper_func in agg_funcs:
            # Perform the grouping and aggregation
            df_for_chart = df_filtered_timerange.groupby(pd.Grouper(key=grouper_key, freq=grouping_freq))[grouper_column].agg(agg_funcs[grouper_func]).reset_index()
            
            # Plot the line chart
            st.line_chart(df_for_chart, x=chart_x, y=chart_y, x_label = chart_label_x, y_label= chart_label_y)
        else:
            st.write(f"Invalid aggregation function selected for {df_key}")

    # # column testing
    # # Create columns
    # col1, col2, col3 = st.columns(3)

    # # Display the total consumption, bill, and average price in the first column
    # with col1:
    #     st.markdown("### Data for the selected period:")
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    #     #st.write(f"**Total bill:** {total_bill:.2f} €")
    #     #st.write(f"**Average price:** {avg_price:.2f} cent / kWh")

    # # Display the min and max price in the second column
    # with col2:
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)

    # # Display the temperature data in the third column
    # with col3:
    #     comsumption = df_filtered_timerange['Energy (kWh)'].sum().round(2)
    
>>>>>>> 41d598a5ad52ccf6734b1c69bb93312761773cea
