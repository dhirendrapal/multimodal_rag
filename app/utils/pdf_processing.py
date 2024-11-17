# app/pdf_processing.py

import os
import fitz  # PyMuPDF for PDF handling
import base64
import streamlit as st

from app.config import client
from langchain_community.document_loaders import PyPDFLoader
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

def extract_images_from_pdf(pdf_path, output_folder, progress_handler):
    pdf_document = fitz.open(pdf_path)
    file_name = os.path.basename(pdf_path)
    dir_name = file_name.split(".")[0]
    output_folder = os.path.join(output_folder, dir_name)
    os.makedirs(output_folder, exist_ok=True)

    total_pages = len(pdf_document)
    img_content = {}

    for page_number in range(total_pages):
        progress_handler.update_progress(page_number, total_pages, f"Processing Page {page_number + 1}/{total_pages}")

        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        combined_text = ""
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
            progress_handler.update_info(f"Extracting text from image {img_index + 1} on Page {page_number + 1}")
            image_description = describe_image(base64_image)
            combined_text += f"\n\n[Image: {image_filename}]\n{image_description}"

        img_content[page_number] = combined_text

    progress_handler.update_progress(total_pages, total_pages, "Processing complete.")
    progress_handler.update_success("PDF processing is complete. Combined text document is ready.")

    return img_content

def load_documents(file_path, images_text):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    for page in pages:
        page.page_content += images_text[page.metadata['page']]

    return pages

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=60,
        separators=["\n\n", "\n"]
    )
    return text_splitter.split_documents(documents)

def create_faiss_index(save_dir, split_docs, progress_handler):
    # Initialize embeddings
    try:
        embedding = OpenAIEmbeddings()  # Replace with your embedding function
        progress_handler.update_info("Initialized embeddings successfully.")
    except Exception as e:
        progress_handler.update_info(f"Error initializing embeddings: {e}")
        return

    os.makedirs(save_dir, exist_ok=True)
    index_path = os.path.join(save_dir, "faiss_index")

    try:
        if os.path.exists(os.path.join(index_path, "index.faiss")) and os.path.exists(
                os.path.join(index_path, "index.pkl")):

            progress_handler.update_info("FAISS index exists. Loading and updating the index.")
            # Load existing index with allow_dangerous_deserialization set to True
            db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)

            initial_count = db.index.ntotal
            db.add_documents(split_docs)
            final_count = db.index.ntotal

            progress_handler.update_info(f"Documents added: {final_count - initial_count} new documents.")
        else:
            progress_handler.update_info("Creating a new FAISS index.")
            db = FAISS.from_documents(split_docs, embedding)
            progress_handler.update_info(f"New FAISS index created with {db.index.ntotal} documents.")

            # Save the index
        db.save_local(index_path)
        progress_handler.update_success(f"FAISS index saved successfully at {index_path}")

    except Exception as e:
        progress_handler.update_info(f"Failed to save FAISS index: {e}")
