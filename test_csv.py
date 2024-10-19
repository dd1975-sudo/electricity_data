import pandas as pd
import streamlit as st

st.write("Hello! Streamlit is working.")


# Streamlit title for the app
st.title("Electricity Data Inspection")

# URL of the electricity data (replace this with the correct URL if needed)
url_electricity = "https://raw.githubusercontent.com/dd1975-sudo/electricity_data/main/Electricity_20-09-2024.csv"


# Load the CSV without specifying usecols to inspect the columns
st.write("Attempting to load the CSV file...")

try:
    df_el = pd.read_csv(url_electricity, delimiter=';', na_values=[''])
    st.write("File loaded successfully!")
    
    # Display the first few rows of the data
    st.write("Preview of the data:")
    st.dataframe(df_el.head())
    
    # Display the column names to help identify the correct ones
    st.write("Columns in the file:")
    st.write(df_el.columns.tolist())
except Exception as e:
    st.error(f"Error loading file: {e}")

# Now that we have inspected the columns, you can update the 'usecols' based on what you found.
# For example, if the column names are slightly different:
# df_el = pd.read_csv(url_electricity, delimiter=';', na_values=[''], usecols=[' Energy (kWh)', 'Temperature'])
