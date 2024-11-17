# app/main.py
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from app.pages.home import app
from app.pages.upload_document import upload_paper_ui
from app.pages.question_answer import question_answer_ui

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload Document", "Q&A"])

# Display the selected page
if page == "Home":
    app()
elif page == "Upload Document":
    upload_paper_ui()
elif page == "Q&A":
    question_answer_ui()

