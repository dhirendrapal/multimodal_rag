# app/pages/summary.py
import streamlit as st


# Mock function for getting a summary
def get_summary(paper_title):
    return f"Summary of {paper_title}: This is a mock summary."


def summary_ui():
    st.title("Research Paper Summary")
    paper_title = st.selectbox("Choose a research paper to summarize", ["Paper 1", "Paper 2", "Paper 3"])

    if paper_title:
        if st.button("Generate Summary"):
            summary = get_summary(paper_title)
            st.write("Summary:")
            st.write(summary)
