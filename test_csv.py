import pandas as pd
import streamlit as st

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
    st.write("
