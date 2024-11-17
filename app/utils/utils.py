import streamlit as st

class ProgressHandler:
    def __init__(self):
        self.progress_placeholder = st.empty()  # For info and success messages
        self.progress_bar = st.progress(0)  # For progress updates

    def update_info(self, message):
        """Update the progress placeholder with an info message."""
        self.progress_placeholder.info(message)

    def update_success(self, message):
        """Update the progress placeholder with a success message."""
        self.progress_placeholder.success(message)

    def update_progress(self, value, total, message):
        """Update the progress bar and message."""
        self.progress_bar.progress(value / total)
        self.progress_placeholder.info(message)

