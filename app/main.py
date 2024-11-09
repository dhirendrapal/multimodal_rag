# app/main.py
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from app.pages.upload_paper import upload_paper_ui
from app.pages.summary import summary_ui
from app.pages.question_answer import question_answer_ui

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Paper", "Summary", "Q&A"])

# Display the selected page
if page == "Upload Paper":
    upload_paper_ui()
elif page == "Summary":
    summary_ui()
elif page == "Q&A":
    question_answer_ui()
