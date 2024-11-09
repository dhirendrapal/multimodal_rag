# app/pages/upload_paper.py
import streamlit as st
from app.utils.file_processing import save_uploaded_file
from app.utils.pdf_processing import (
    extract_images_and_text_from_pdf,
    load_documents,
    create_faiss_index
)
import time

def upload_paper_ui():
    st.title("Upload Research Paper")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        # Step 1: Upload PDF
        with st.spinner("Uploading file..."):
            file_path = save_uploaded_file(uploaded_file)
        st.success(f"File '{uploaded_file.name}' uploaded and saved successfully!")
        st.write(f"Saved at: {file_path}")

        # Step 2: Extract images and text from PDF
        st.info("Extracting images and text from PDF...")
        combined_text = extract_images_and_text_from_pdf(file_path, 'extracted_images_new')

        # Step 3: Save all text in a text file
        st.info("Saving extracted text to a file...")
        with open("combined_text.txt", "w") as text_file:
            text_file.write(combined_text)
        st.success("Text saved to 'combined_text.txt'.")

        # Step 4: Load text documents
        st.info("Loading text documents...")
        split_docs = load_documents("combined_text.txt")
        st.info(f"docs lenght: {len(split_docs)}")
        st.success("Text documents loaded.")

        # Step 5: Split text documents into chunks
        st.info("Splitting text into chunks...")
        # The function `load_documents` already returns split documents
        # so no additional code needed here, only displaying progress.
        time.sleep(1)
        st.success("Text documents split into chunks.")
        # Step 6: Create embeddings for chunks and save using FAISS
        st.info("Creating FAISS index and saving embeddings...")
        create_faiss_index('data/embeddings', split_docs)
        st.success("FAISS index created and embeddings saved.")

        return file_path
    else:
        st.info("Please upload a PDF file.")