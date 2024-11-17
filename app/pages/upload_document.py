# app/pages/upload_paper.py
import streamlit as st
from app.utils.utils import ProgressHandler
from app.utils.file_processing import save_uploaded_file
from app.utils.pdf_processing import (
    extract_images_from_pdf,
    load_documents,
    split_documents,
    create_faiss_index
)
import time

def upload_paper_ui():
    st.title("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        # Initialize ProgressHandler
        progress = ProgressHandler()
        # Step 1: Upload PDF
        with st.spinner("Uploading file..."):
            file_path = save_uploaded_file(uploaded_file)
        progress.update_success(f"File '{uploaded_file.name}' uploaded and saved successfully!")

        # Step 2: Extract images from PDF
        progress.update_info("Extracting images from PDF...")
        images_text = extract_images_from_pdf(file_path, 'extracted_images_new', progress)

        # Step 3: Load documents
        progress.update_info("Loading documents...")
        documents = load_documents(file_path, images_text)
        progress.update_success("Documents loaded.")

        # Step 4: Split text documents into chunks
        progress.update_info("Splitting documents into chunks...")
        split_docs = split_documents(documents)
        time.sleep(1)
        progress.update_success("Documents split into chunks.")

        # Step 5: Create embeddings for chunks and save using FAISS
        progress.update_info("Creating FAISS index and saving embeddings...")
        create_faiss_index('data/embeddings', split_docs, progress)
        progress.update_success("FAISS index created and embeddings saved.")

        return file_path
    else:
        st.info("Please upload a PDF file.")