import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
import pytesseract
from PyPDF2 import PdfReader
import os
import time
import json
from io import BytesIO
import re

# Set the path to the Tesseract executable (change this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

global ocr_text
def get_csv_files_in_folder(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    return csv_files

# Declare ocr_text as a global variable
ocr_text_global = ocr_text

def find_matching_paragraphs(data, phrases):
    paragraphs = data.split("\n\n")  # Assuming paragraphs are separated by two newlines
    matching_paragraphs = []
    for phrase in phrases:
        for paragraph in paragraphs:
            if phrase in paragraph:
                matching_paragraphs.append(paragraph.strip())
                break  # Break once a matching paragraph is found for the current phrase
    return matching_paragraphs if matching_paragraphs else ["No matching paragraphs found"]

# Dummy multiple-paragraph data


phrases_to_search = ["end of the contractual relation", "ends of the contract", "settlement"]  # Phrases to search for

matching_paragraphs = find_matching_paragraphs(ocr_text, phrases_to_search)

print("Matching Paragraphs:")
for idx, paragraph in enumerate(matching_paragraphs, 1):
    print(f"Match {idx}:")
    print(paragraph)
    print()





def read_pdf(file, page_num):
    pdf_reader = PdfReader(file)
    text = ""
    if page_num < len(pdf_reader.pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
    return text


# Add these variables at the beginning of your script, before using them
# font_size = 14
# draw = None
# font = None
# ocr_text = ""

# List of phrases to match in OCR text
end_contract_phrases = [
    "end of the contractual relation",
    "ends of the contract",
    "settlement",
    "end of the contract",
]

# Function to find paragraph locations in text
def find_paragraph_locations(text, phrases):
    locations = []

    for phrase in phrases:
        start = 0
        while start < len(text):
            index = text.find(phrase, start)
            if index == -1:
                break

            # Find the start and end of the paragraph containing the phrase
            paragraph_start = text.rfind('\n', 0, index) + 1
            paragraph_end = text.find('\n', index)
            if paragraph_end == -1:
                paragraph_end = len(text)

            locations.append((paragraph_start, paragraph_end))
            start = index + len(phrase)

    return locations

# Modify the perform_analysis function to include the new functionality
def perform_analysis(image, language='ara', ocr_engine='lstm'):
    global draw, font, font_size, ocr_text  # Add these global declarations
    try:
        # Try OCR using pytesseract with specified language and engine
        ocr_text = pytesseract.image_to_string(image, lang=language, config=f'--oem 3 --psm 6')

        # Initialize draw and font objects
        draw = ImageDraw.Draw(image)
        font = None  # Use default font

        # Find paragraph locations containing specified phrases
        paragraph_locations = find_paragraph_locations(ocr_text.lower(), end_contract_phrases)

        # Highlight entire paragraphs in OCR text
        for start_index, end_index in paragraph_locations:
            line_num, line_pos = find_line_and_position(ocr_text, start_index)
            x = line_pos * font_size
            y = line_num * font_size
            width = (end_index - start_index) * font_size
            height = font_size

            # Draw the rectangle with red outline
            draw.rectangle([x, y, x + width, y + height], outline=(255, 0, 0), width=2)

            # Draw the text in black color inside the rectangle
            draw.text((x, y), ocr_text[start_index:end_index], font=font, fill=(0, 0, 0))

        return ocr_text
    except Exception as e:
        print(f"OCR failed: {e}")
        return "OCR failed"

# Inside the main function, after the OCR analysis
# Check if there are matches for end contract phrases and highlight the paragraphs
for phrase in end_contract_phrases:
    if phrase.lower() in ocr_text.lower():
        st.subheader(f"Matching Information for '{phrase}':")
        st.text_area(f"Matching Paragraph:", ocr_text, height=200)


# Continue with the rest of the code...



def highlight_matching_data(csv_data, ocr_text):
    matches = {}
    for record in csv_data:
        for key, value in record.items():
            if str(value).lower() in str(ocr_text).lower():
                matches[key] = value
    return matches


def find_substring_locations(text, substring):
    locations = []
    start = 0

    while start < len(text):
        index = text.find(substring, start)
        if index == -1:
            break
        locations.append((index, index + len(substring)))
        start = index + len(substring)

    return locations


def draw_rectangles_on_pdf(pdf_text, matches, page_number):
    pdf_image = Image.new("RGB", (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(pdf_image)
    font_size = 14
    font = None  # Use default font

    marked_text = pdf_text

    for match in matches.values():
        locations = find_substring_locations(marked_text.lower(), match.lower())

        for start_index, end_index in locations:
            line_num, line_pos = find_line_and_position(marked_text, start_index)
            x = line_pos * font_size
            y = line_num * font_size
            width = (end_index - start_index) * font_size
            height = font_size

            # Draw the rectangle with red outline
            draw.rectangle([x, y, x + width, y + height], outline=(255, 0, 0), width=2)

            # Draw the text in black color inside the rectangle
            draw.text((x, y), match, font=font, fill=(0, 0, 0))

    draw.text((10, 580), f"Page {page_number + 1}", font=font, fill=(0, 0, 0))

    return pdf_image


def draw_rectangles_on_image(image, matches, ocr_text):
    marked_image = image.copy()
    draw = ImageDraw.Draw(marked_image)

    for match in matches.values():
        locations = find_substring_locations(ocr_text.lower(), match.lower())

        for start_index, end_index in locations:
            x, y, width, height = start_index, 0, end_index - start_index, marked_image.height

            # Draw the rectangle with red outline
            draw.rectangle([x, y, x + width, y + height], outline=(255, 0, 0), width=2)

            # Draw the text in black color inside the rectangle
            draw.text((x, y), match, fill=(0, 0, 0))

    # Display all OCR text in the image
    draw.text((10, 10), "OCR Text:", font=None, fill=(0, 0, 0))
    draw.text((10, 30), ocr_text, font=None, fill=(0, 0, 0))

    return marked_image


def preview_pdf_page(pdf_text, matches, page_number, matching_pages):
    pdf_image = draw_rectangles_on_pdf(pdf_text, matches, page_number)
    marked_image = draw_rectangles_on_image(pdf_image, matches, pdf_text)

    st.subheader("Preview of PDF Page with Matching Areas:")

    # Convert the marked image to bytes and display with st.image
    img_bytes = BytesIO()
    marked_image.save(img_bytes, format='PNG')
    st.image(img_bytes, caption=f"Page {page_number + 1} - Marked PDF", use_column_width=True)

    # Add download button for the marked image
    download_button = st.download_button(
        label="Download Marked Image",
        data=img_bytes.getvalue(),
        file_name=f"marked_page_{page_number + 1}.png",
        key=f"download_button_{page_number}",
    )

    # Check if there are matches and add a link for the matching page
    if matches:
        matching_pages.append({"page_number": page_number, "matches": matches})

    # Display matching information for all matching pages
    for matching_info in matching_pages:
        matching_page_number = matching_info["page_number"]
        matching_matches = matching_info["matches"]
        matching_link = f"[Page {matching_page_number + 1} - Matching Information](#matching_page_{matching_page_number})"
        st.markdown(matching_link, unsafe_allow_html=True)

        # Use st.expander to create an expandable section for matching information
        with st.expander(f"Matching Information in (Page {matching_page_number + 1}):", expanded=False):

            st.text_area(f"Matching Information:", json.dumps(matching_matches, indent=2), height=200)




# Function to create a download link for an image
def get_image_download_link(img_bytes, file_name, text="Download Marked Image"):
    href = f'<a href="data:file/png;base64,{img_bytes}" download="{file_name}">{text}</a>'
    return href


def find_line_and_position(text, index):
    lines = text.split('\n')
    current_index = 0
    for i, line in enumerate(lines):
        current_index += len(line) + 1
        if current_index > index:
            return i, index - (current_index - len(line) - 1)

    return len(lines) - 1, len(lines[-1]) - 1


def main():
    topic = ["Work pay request", "Contract termination request"]  # Replace with your options
    required_attachment = ["attach the job contract", "attach the job contract + bank statement"]
    # reason = st.selectbox("Reason:", reason_options)
    col1, col2 = st.columns(2)
    with col1:
        # st.header("Column 1")
        topic = st.selectbox("Case Topic", topic)
    with col2:
        # st.header("Column 2")
        sub_topic = st.selectbox("Case required attachment", required_attachment)



    # List all CSV files in the 'csv' directory
    csv_directory = 'csv'
    csv_files = get_csv_files_in_folder(csv_directory)

    # Let the user choose a CSV file
    selected_csv_file = st.selectbox("Choose a CSV file", csv_files, index=0)

    # Display selected CSV file name
    st.write(f"Selected CSV file: {selected_csv_file}")

    # Load CSV data based on the user's choice
    csv_file_path = os.path.join(csv_directory, selected_csv_file)
    csv_data = pd.read_csv(csv_file_path).to_dict(orient='records')

    st.title("File Attachment")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg"])

    # Initialize ocr_text
    ocr_text = ""
    matching_pages = []  # List to store pages with matching information

    if uploaded_file is not None:
        # Display file information in six columns
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Column 1: Display file name and size
        file_name = os.path.basename(uploaded_file.name)
        file_size = f"{uploaded_file.size / 1024:.1f} KB"
        col1.write(file_name)
        col5.write(file_size)

        # Columns 2-4: Placeholder columns
        col2.write("")
        col3.write("")
        col4.write("")

        # Column 6: Delete button
        delete_button = col6.button("Delete File")

        if delete_button:
            # Confirm file deletion
            confirmation = st.confirm(f"Are you sure you want to delete {file_name}?")
            if confirmation:
                # Delete the file
                st.warning(f"File {file_name} deleted.")
                uploaded_file = None  # Reset the uploaded file

        # Check if uploaded_file is not None before accessing its attributes
        if uploaded_file is not None:
            file_type = uploaded_file.type

            # Display all CSV data in a text box with JSON format
            st.subheader("User input data to be analysed:")
            st.text_area("User input data:", json.dumps(csv_data, indent=2), height=200)

            if file_type == "application/pdf":
                # Page selection for PDF
                selected_page = st.number_input("Enter Page Number (starting from 0)", value=0, min_value=0)
                st.subheader(f"PDF File Content (Page {selected_page + 1})")
                pdf_text = read_pdf(uploaded_file, selected_page)
                if pdf_text is not None:
                    st.text_area("Extracted Text:", pdf_text, height=200)
                    ocr_text = pdf_text  # Set ocr_text for PDF

                    # Highlight matching data from CSV file
                    matches = highlight_matching_data(csv_data, ocr_text)

                    # Display matching information
                    st.subheader(f"Matching Information from user in (Page {selected_page + 1}) :")
                    if matches:
                        st.write(matches)

                        # User feedback
                        user_feedback = st.checkbox("This Information is Correct From User")
                        if user_feedback:
                            st.success("User confirmed that the information is correct.")

                        # Display wrong information
                        wrong_info = {key: value for key, value in csv_data[0].items() if key not in matches}
                        if wrong_info:
                            st.subheader(f"No Matching Information from user in (Page {selected_page + 1}) :")
                            st.write(wrong_info)
                    else:
                        st.warning(f"No Matching Information from user in (Page {selected_page + 1}) :")

                        # Display all CSV data when there are no matches
                        st.subheader("No Matching Information in CSV:")
                        st.text_area("CSV Data:", json.dumps(csv_data, indent=2), height=200)

                    # Preview PDF page with matching areas
                    preview_pdf_page(pdf_text, matches, selected_page, matching_pages)

            elif file_type == "image/jpeg" or file_type == "image/jpg":
                st.subheader("JPG File Display")
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded JPG", use_column_width=True)

                # Display text area for OCR result
                st.subheader("Analysis Result")
                ocr_result_text_area = st.empty()

                # Analysis button below the text area
                analysis_button = st.button("Analysis", key="analysis_button")

                if analysis_button:
                    with st.spinner("Analyzing..."):
                        # Simulating analysis time (adjust based on actual analysis time)
                        time.sleep(2)
                        # Perform OCR on the image with specified language
                        ocr_text = perform_analysis(image, language='ara')
                        ocr_result_text_area.text_area("Extracted Text:", ocr_text, height=200)

                        # Highlight matching data from CSV file
                        matches = highlight_matching_data(csv_data, ocr_text)

                        # Display matching information
                        st.subheader("Matching Information from CSV:")
                        if matches:
                            st.write(matches)

                            # User feedback
                            user_feedback = st.checkbox("This Information is Correct From User ")
                            if user_feedback:
                                st.success("User confirmed that the information is correct.")

                            # Display wrong information
                            wrong_info = {key: value for key, value in csv_data[0].items() if key not in matches}
                            if wrong_info:
                                st.subheader("Incorrect Information:")
                                st.write(wrong_info)
                        else:
                            st.warning("No Matching Information between CSV file and OCR text.")

                            # Display all CSV data when there are no matches
                            st.subheader("No Matching Information in CSV:")
                            st.text_area("CSV Data:", json.dumps(csv_data, indent=2), height=200)

                        # Preview image with matching areas
                        marked_image = draw_rectangles_on_image(image, matches, ocr_text)
                        st.subheader("Marked JPG Image:")
                        # Convert the marked image to bytes and display with st.image
                        img_bytes = BytesIO()
                        marked_image.save(img_bytes, format='PNG')
                        st.image(img_bytes, caption="Marked JPG", use_column_width=True)

                        # Display matching information for each matching page
                        for page_number in matching_pages:
                            with st.expander(f"Matching Information in (Page {page_number + 1}):", expanded=False):
                                matching_info = highlight_matching_data(csv_data, ocr_text)
                                st.text_area(f"Matching Information:", json.dumps(matching_info, indent=2), height=200)


if __name__ == "__main__":
    main()

