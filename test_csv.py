# testing csv
import pandas as pd

# URL of the electricity data (replace this with the correct one if needed)
url_electricity = "https://raw.githubusercontent.com/dd1975-sudo/electricity_data/refs/heads/main/Electricity_20-09-2024.csv"

# Load the CSV without specifying usecols to inspect the columns
try:
    df_el = pd.read_csv(url_electricity, delimiter=';', na_values=[''])
    print("Columns in the file:", df_el.columns)
except Exception as e:
    print("Error loading file:", e)

# Once you know the exact column names, adjust the usecols to match
# For example, if you find the columns are named something like ' Energy (kWh)' (with a leading space),
# you can adjust it like this:
# df_el = pd.read_csv(url_electricity, delimiter=';', na_values=[''], usecols=[' Energy (kWh)', 'Temperature'])
