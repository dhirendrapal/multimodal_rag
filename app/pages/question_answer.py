# app/pages/question_answer.py
# app/pages/question_answer.py
import streamlit as st
from app.utils.question_answering_service import ask_question_with_images

def question_answer_ui():
    st.title("Question and Answer")
    question = st.text_input("Enter your question")

    if question and st.button("Get Answer"):
        answer, page_number, image_references = ask_question_with_images(question)

        # Display the answer and page number
        st.write("Answer:")
        st.write(answer)
        st.write(f"Referenced Page: {page_number}")

        # Display image references
        if image_references:
            st.write("Referenced Images:")
            for image_ref in image_references:
                st.image(f"extracted_images_new/{image_ref}")
        else:
            st.write("No referenced images found.")


