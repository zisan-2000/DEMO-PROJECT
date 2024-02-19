import streamlit as st
import csv
import os

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Termination Clause", "Bank Name", "IBAN No"])
        for row in data:
            csv_writer.writerow(row)

def main():
    st.title("Termination Clause and Banking Information Form")

    # User form
    termination_clause_option = st.selectbox("Do you have Termination Clause Mentioned in your job Contract?",
                                             ["Yes", "No"])
    if termination_clause_option == "Yes":
        termination_clause_options = [
            "end of the contractual relation",
            "ends of the contract",
            "end of the contract"
        ]
        selected_clauses = st.multiselect("Select Termination Clauses:", termination_clause_options)
    bank_name = st.text_input("Enter Bank Name:")
    iban_no = st.text_input("Enter IBAN No:")
    submit_button = st.button("Submit")



    if submit_button:
        if termination_clause_option == "Yes":
            # Save to CSV
            csv_folder = "csv"
            os.makedirs(csv_folder, exist_ok=True)
            file_path = os.path.join(csv_folder, "termination_data.csv")
            data_to_save = [(clause, bank_name, iban_no) for clause in selected_clauses]
            save_to_csv(data_to_save, file_path)

            st.success("Data saved successfully!")

if __name__ == "__main__":
    main()
