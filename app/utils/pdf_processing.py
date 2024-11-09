# app/pdf_processing.py

import os
import fitz  # PyMuPDF for PDF handling
import base64
import streamlit as st

from app.config import client
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import tiktoken

def describe_image(base64_image):
    """
    Uses OpenAI's GPT-4o model to generate a description of the image.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Your job is to extract all the information from the images, including the text. Extract all the text from the image without changing the order or structure of the information."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract ALL the text from the image in the same structure, and then provide a brief summary without missing any details."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                },
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error in describe_image: {e}")
        return "Error describing image."

def extract_images_and_text_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)
    combined_text = ""
    total_pages = len(pdf_document)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for page_number in range(total_pages):
        progress_bar.progress(page_number / total_pages)
        status_text.text(f"Processing Page {page_number + 1}/{total_pages}")

        page = pdf_document.load_page(page_number)
        text = page.get_text()
        combined_text += f"\n\nPage {page_number + 1}:\n{text}"
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}"
            image_filepath = os.path.join(output_folder, image_filename)

            with open(image_filepath, "wb") as image_file:
                image_file.write(image_bytes)

            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            status_text.text(f"Describing image {img_index + 1} on Page {page_number + 1}")
            image_description = describe_image(base64_image)
            combined_text += f"\n\n[Image: {image_filename}]\n{image_description}"
            st.info(f"Processed {image_filename} on page {page_number + 1}")

    progress_bar.progress(1.0)
    status_text.text("Processing complete.")
    st.success("PDF processing is complete. Combined text document is ready.")

    return combined_text

def load_documents(file_path):
    loaders = TextLoader(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=60,
        separators=["\n\n", "\n"]
    )
    return text_splitter.split_documents(loaders.load())

def create_faiss_index(save_dir, split_docs):
    # Initialize embeddings
    try:
        embedding = OpenAIEmbeddings()  # Replace with your embedding function
        st.info("Initialized embeddings successfully.")
    except Exception as e:
        st.error(f"Error initializing embeddings: {e}")
        return

    os.makedirs(save_dir, exist_ok=True)
    index_path = os.path.join(save_dir, "faiss_index")

    try:
        # Check if an index already exists
        if os.path.exists(f"{index_path}.faiss") and os.path.exists(f"{index_path}.pkl"):
            st.info("FAISS index exists. Loading and updating the index.")
            db = FAISS.load_local(index_path, embedding)
            st.info("Index loaded. Adding new documents to the index.")
            db.add_documents(split_docs)
            st.info(f"Documents added to index. New total: {db.index.ntotal} at {index_path}")
        else:
            st.info("Creating a new FAISS index.")
            db = FAISS.from_documents(split_docs, embedding)
            st.info(f"New FAISS index created with {db.index.ntotal} documents.")

        # Save the updated or newly created index
        db.save_local(index_path)
        st.success(f"FAISS index saved successfully at {index_path}")
    except Exception as e:
        st.error(f"Failed to save FAISS index: {e}")
