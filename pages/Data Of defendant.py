import streamlit as st

# Initialize st.session_state
if 'my_input' not in st.session_state:
    st.session_state.my_input = None

st.title("Data of Defendant")

# Checkbox
# Check if the checkbox is checked
# Title of the checkbox is 'Add international number'
defendant_type = st.radio("Type of defendant Government Agencies/Non-Government: ",
                         ('Type of defendant Government Agencies ', 'Non-Government'))

# Dropdown text box for "The name of establishment"
establishment_name_options = ["Option 1", "Option 2", "Option 3", "Other"]
establishment_name = st.selectbox("The name of establishment", establishment_name_options)

# If "Other" is selected, show a text input field
if establishment_name == "Other":
    custom_establishment_name = st.text_input("Enter the custom establishment name", "")

# Two columns layout
col1, col2 = st.columns(2)

# Placeholder values for the form
default_values_column1 = {
    'City': '',
    'Street': '',
    'Postal Code': ''
}

default_values_column2 = {
    'Region': '',
    'Neighborhood': '',
    'Building Name': '',
    'The Additional No': ''
}

# Column 1: City, Street, Postal Code
with col1:
    #st.header("Column 1")
    city = st.text_input("City", default_values_column1['City'])
    street = st.text_input("Street", default_values_column1['Street'])
    postal_code = st.text_input("Postal Code", default_values_column1['Postal Code'])

# Column 2: Region, Neighborhood, Building Name, The Additional No
with col2:
    #st.header("Column 2")
    region = st.text_input("Region", default_values_column2['Region'])
    neighborhood = st.text_input("Neighborhood", default_values_column2['Neighborhood'])
    building_name = st.text_input("Building Name", default_values_column2['Building Name'])
    additional_no = st.text_input("The Additional No", default_values_column2['The Additional No'])

# Button to submit the form
if st.button("Submit"):
    # Do something with the form data, e.g., store it or perform an action
    # You can access the values entered in the form like city, street, region, etc.
    st.success("Form submitted successfully!")
