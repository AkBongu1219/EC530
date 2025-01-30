import streamlit as st
import pandas as pd
import os
from EC530_HW2.EC530_2 import (
    haversine,
    parse_coordinate,
    match_closest_points,
    read_coordinates_from_csv
)

# Streamlit App Title
st.title("📍 Geolocation Matcher - EC530_HW2")

# Sidebar for user input mode selection
st.sidebar.header("User Input Mode")
input_mode = st.sidebar.radio(
    "Choose how to input data:", 
    ("Enter Coordinates Manually", "Upload CSV Files")
)

# Function to format results
def display_matches(matches):
    st.subheader("📌 Closest Point Matches")
    df_results = pd.DataFrame(matches, columns=["Point 1", "Closest Point", "Distance (km)"])
    st.dataframe(df_results)

### MANUAL COORDINATE INPUT ###
if input_mode == "Enter Coordinates Manually":
    st.subheader("📝 Enter Coordinates")
    
    num_points = st.number_input("Number of points per list:", min_value=1, value=2, step=1)

    array1 = []
    array2 = []

    st.write("### Array 1 Coordinates")
    for i in range(num_points):
        col1, col2 = st.columns(2)
        with col1:
            lat = st.text_input(f"Latitude {i+1} (e.g., 45.678 or 45°30'15\" N)")
        with col2:
            lon = st.text_input(f"Longitude {i+1} (e.g., -120.123 or 120°15'30\" W)")
        if lat and lon:
            parsed_lat = parse_coordinate(lat)
            parsed_lon = parse_coordinate(lon)
            if parsed_lat is not None and parsed_lon is not None:
                array1.append((parsed_lat, parsed_lon))

    st.write("### Array 2 Coordinates")
    for i in range(num_points):
        col1, col2 = st.columns(2)
        with col1:
            lat = st.text_input(f"Latitude {i+1} (Array 2)")
        with col2:
            lon = st.text_input(f"Longitude {i+1} (Array 2)")
        if lat and lon:
            parsed_lat = parse_coordinate(lat)
            parsed_lon = parse_coordinate(lon)
            if parsed_lat is not None and parsed_lon is not None:
                array2.append((parsed_lat, parsed_lon))

    if st.button("🔎 Find Closest Points"):
        if array1 and array2:
            matches = match_closest_points(array1, array2)
            display_matches(matches)
        else:
            st.error("Please enter valid coordinates.")

### CSV UPLOAD MODE ###
elif input_mode == "Upload CSV Files":
    st.subheader("📂 Upload CSV Files")

    file1 = st.file_uploader("Upload First CSV (Array 1)", type=["csv"])
    file2 = st.file_uploader("Upload Second CSV (Array 2)", type=["csv"])

    if file1 and file2:
        array1 = read_coordinates_from_csv(file1)
        array2 = read_coordinates_from_csv(file2)

        if st.button("🔎 Find Closest Points"):
            if array1 and array2:
                matches = match_closest_points(array1, array2)
                display_matches(matches)
            else:
                st.error("Invalid CSV files. Please upload valid coordinate data.")

# Footer
st.markdown("---")
st.markdown("🚀 **Developed for EC530_HW2** | Streamlit Geolocation Matcher")