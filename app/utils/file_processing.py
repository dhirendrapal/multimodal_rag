# app/utils/file_processing.py
import os

# Directory to save uploaded files
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/saved_documents")

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(uploaded_file):
    # Step 1: Transform the file name
    original_file_name = uploaded_file.name
    file_name, file_extension = os.path.splitext(original_file_name)
    transformed_file_name = file_name.lower().replace(" ", "_") + file_extension

    # Step 2: Define the file path to save
    save_path = os.path.join(UPLOAD_FOLDER, transformed_file_name)

    # Step 3: Save the file
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    return save_path