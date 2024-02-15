import streamlit as st
import pandas as pd
from datetime import datetime
import os

CSV_FILE_PATH = 'csv/Bank_Statement.csv'


# Function to save data to CSV
def save_to_csv(data):
    df = pd.DataFrame([data])

    if not os.path.isfile(CSV_FILE_PATH):
        df.to_csv(CSV_FILE_PATH, index=False)
    else:
        df.to_csv(CSV_FILE_PATH, mode='a', index=False, header=False)


# Streamlit App
def main():
    st.title("Second Party's Bank Account Information (user input)")

    # Date Input for termination Contract
    termination_contract = st.text_input("Do you have Termination Clause Mentioned in your job Contract ")
    hc_termination_cl="Paying the first party's wages "
    # Text Inputs for Bank Name and IBAN
    bank_name = st.text_input("Bank Name")
    iban = st.text_input("IBAN")

    # Submit Button
    if st.button("Submit"):
        data = {
            "Termination Contract Information": hc_termination_cl,
            "Bank Name": bank_name,
            "IBAN": iban
        }
        save_to_csv(data)
        st.success("Data saved successfully!")


if __name__ == "__main__":
    main()
