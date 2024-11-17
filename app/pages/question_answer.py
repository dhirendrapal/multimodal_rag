# app/pages/question_answer.py
import os
import streamlit as st
from app.utils.question_answering_service import ask_question_with_images
import matplotlib.pyplot as plt

def question_answer_ui():
    st.title("Question and Answer")
    question = st.text_input("**Enter your question**", label_visibility="visible")

    if question and st.button("Get Answer"):
        answer, page_number, page_source, image_references = ask_question_with_images(question)

        # Display the answer and page number
        st.markdown("**Answer:**")
        st.write(answer)
        st.markdown(f"**Referenced documents:** {page_source}")
        st.markdown(f"**Referenced Page:** {(page_number+1)}")

        # Display image references
        if image_references:
            doc_img_src = page_source.split(".")[0]
            st.markdown("**Referenced Images:**")
            for image_ref in image_references:
                image_ref = os.path.join(doc_img_src, image_ref)
                # Check if the image reference is a plot or an image file
                if isinstance(image_ref, plt.Figure):
                    st.pyplot(image_ref)  # Display the plot if it's a Matplotlib figure
                else:
                    st.image(f"extracted_images_new/{image_ref}")  # Display as an image if it's a file path
        else:
            st.write("No referenced images found.")


