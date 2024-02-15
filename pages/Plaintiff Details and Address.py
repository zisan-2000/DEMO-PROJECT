import streamlit as st
import pandas as pd

# Initialize st.session_state
if 'my_input' not in st.session_state:
    st.session_state.my_input = None

# Placeholder values for the form
default_values_column1 = {
    'Id': '',
    'City': '',
    'gender': '',
    'birth_date': '',
    'Street': '',
    'Postal Code': ''
}

default_values_column2 = {
    'Region': '',
    'Neighborhood': '',
    'Building Name': '',
    'Mobile No': '',
    'job title': '',
    'work location': ''
}

# Checkbox
# Check if the checkbox is checked
# Title of the checkbox is 'Add international number'
if st.checkbox("Add international number"):
    # Display the text if the checkbox returns True value
    st.text("Showing the widget")

# Title of the form
st.title("Plaintiff Address Form")

# Two columns layout
col1, col2 = st.columns(2)

# Column 1: City, Street, Postal Code
with col1:
    st.header("Column 1")
    Id = st.text_input("Id", default_values_column1['Id'])
    city = st.text_input("City", default_values_column1['City'])
    gender = st.text_input("gender", default_values_column1['gender'])
    birth_date = st.text_input("birth_date", default_values_column1['birth_date'])
    street = st.text_input("Street", default_values_column1['Street'])
    postal_code = st.text_input("Postal Code", default_values_column1['Postal Code'])

# Column 2: Region, Neighborhood, Building Name, The Additional No
with col2:
    st.header("Column 2")
    region = st.text_input("Region", default_values_column2['Region'])
    neighborhood = st.text_input("Neighborhood", default_values_column2['Neighborhood'])
    building_name = st.text_input("Building Name", default_values_column2['Building Name'])
    Mobile_No = st.text_input("Mobile No", default_values_column2['Mobile No'])
    job_title = st.text_input("job title", default_values_column2['job title'])
    work_location = st.text_input("work location", default_values_column2['work location'])

# Button to submit the form
if st.button("Submit"):
    # Create a DataFrame with the form data
    data = {
        'Id': [Id],
        'City': [city],
        'gender': [gender],
        'birth_date': [birth_date],
        'Street': [street],
        'Postal Code': [postal_code],
        'Region': [region],
        'Neighborhood': [neighborhood],
        'Building Name': [building_name],
        'Mobile No': [Mobile_No],
        'job title': [job_title],
        'work location': [work_location]
    }

    # Check if the CSV file exists
    try:
        df = pd.read_csv('csv/plaintiff_address_data.csv')
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame()

    # Concatenate the new data with the existing DataFrame
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    # Save the updated DataFrame to the CSV file
    df.to_csv('csv/plaintiff_address_data.csv', index=False)

    # Display a success message
    st.success("Form submitted successfully! Data saved to 'plaintiff_address_data.csv'")
