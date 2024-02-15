import streamlit as st
from ArabicOcr import arabicocr
import fitz
import cv2
import os


# Function to upload a PDF file in Streamlit
def upload_pdf():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with open("input.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("PDF uploaded successfully!")


# Function to perform OCR on the selected page
def perform_ocr(page_number, target_words):
    pdf_path = "input.pdf"
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Get the selected page
    page = doc[page_number]

    # Render page to an image
    pix = page.get_pixmap()
    image_path = os.path.join(output_folder, f"page_{page.number}.png")
    pix.save(image_path)

    # Perform Arabic OCR on the image
    out_image = os.path.join(output_folder, f"out_{page.number}.jpg")
    results = arabicocr.arabic_ocr(image_path, out_image)

    # Process OCR results
    words = []
    annotations = []

    for i in range(len(results)):
        word = results[i][1]
        annotation = results[i][0]

        words.append(word)
        annotations.append(annotation)

    # Write results to text files
    with open(f'file_page_{page.number}.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(str(words))

    with open(f'annotations_page_{page.number}.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(str(annotations))

    # Display OCR result
    img = cv2.imread(out_image, cv2.IMREAD_UNCHANGED)
    st.image(img, caption=f"OCR Result - Page {page.number + 1}", use_column_width=True)

    # Search for target words in OCR results
    target_words_found = [word for word in target_words if any(word in w for w in words)]

    if target_words_found:
        st.success(f"Target words '{', '.join(target_words_found)}' found in OCR results!")
    else:
        st.warning("Target words not found in OCR results.")


# Main Streamlit app
def main():
    st.title("Arabic OCR Analysis on PDF Pages")

    # Step 1: Upload PDF
    st.header("Step 1: File Attachment ")
    upload_pdf()

    # Step 2: Perform OCR for the selected page
    st.header("Step 2: Perform OCR ANALYSIS")
    page_number = st.selectbox("Select Page", range(1, 101), key="page_number")
    target_words = st.text_input("Enter target words (comma-separated)", "Ehab Mohammed ").split(',')

    if st.button("ANALYSIS"):
        perform_ocr(page_number - 1, target_words)  # Adjust index since page numbers start from 1

    # Navigation to the next page
    if st.button("+"):
        page_number += 1
        if page_number > 100:  # Assuming a maximum of 100 pages
            page_number = 1
        st.session_state.page_number = page_number


if __name__ == "__main__":
    main()
