import pandas as pd
import streamlit as st

# Streamlit title for the app
st.title("Electricity Data Inspection")

# URL of the electricity data
url_electricity = "https://raw.githubusercontent.com/dd1975-sudo/electricity_data/main/Electricity_20-09-2024.csv"

# Display a message to verify Streamlit is running
st.write("Hello! Streamlit is working.")

# Try to load specific columns from the CSV file
st.write("Loading CSV file with specific columns...")
try:
    # Adjust the usecols argument based on the correct column names
    df_el = pd.read_csv(url_electricity, delimiter=';', na_values=[''], usecols=['Energy (kWh)', 'Temperature'])
    
    st.write("File loaded successfully with specified columns!")
    
    # Display the first few rows of the selected columns
    st.write("Preview of the selected data:")
    st.dataframe(df_el.head())
    
except Exception as e:
    st.write(f"Error loading file: {e}")
