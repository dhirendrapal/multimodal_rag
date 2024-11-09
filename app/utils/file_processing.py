# app/utils/file_processing.py
import os

# Directory to save uploaded files
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/saved_documents")

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(uploaded_file):
    """
    Save the uploaded file to the specified upload folder.

    Args:
        uploaded_file: The file uploaded by the user in Streamlit.

    Returns:
        str: The file path where the uploaded file is saved.
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
