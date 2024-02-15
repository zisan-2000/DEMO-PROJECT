import streamlit as st
from ArabicOcr import arabicocr
import fitz
import cv2
import matplotlib.pyplot as plt
import os

# Function to upload a PDF file in Streamlit
def upload_pdf():
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with open("input.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("PDF uploaded successfully!")

# Function to perform OCR on the uploaded PDF
def perform_ocr():
    pdf_path = "input.pdf"
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF document
    doc = fitz.open(pdf_path)

    for page in doc:
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

# Main Streamlit app
def main():
    st.title("Arabic OCR Analysis on PDF Pages")

    # Step 1: Upload PDF
    st.header("Step 1: Upload Attachment ")
    upload_pdf()

    # Step 2: Perform OCR
    st.header("Step 2: Perform and Analysis OCR")
    if st.button("ANALYSIS"):
        perform_ocr()

if __name__ == "__main__":
    main()
