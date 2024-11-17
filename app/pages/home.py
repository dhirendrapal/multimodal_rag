import streamlit as st

def app():
    st.title("Welcome to Multimodal RAG")
    st.subheader("Multimodal RAG")

    st.write("""
    Multimodal Retrieval-Augmented Generation (RAG) is an advanced AI system that combines multiple types of data—such as text, images, and potentially other modalities like audio or video—to enhance the capabilities of language models in generating accurate and contextually relevant responses. In a standard RAG system, textual data is typically used, but in a multimodal setup, the system can retrieve and process information from multiple types of data (text, images, etc.) simultaneously.
    """)

    st.subheader("Why is Multimodal RAG Needed?")
    st.write("""
    - **Images and Text Together:**  
    Many real-world scenarios involve both visual and textual information. For example, a medical report might include both a doctor's notes (text) and X-ray images. A standard text-only RAG system would miss the visual context, potentially leading to incomplete or incorrect responses. By incorporating images, a multimodal RAG system can fully understand and generate more accurate answers.

    - **Complementary Information:**
     Text and images often provide complementary information. A diagram in a technical document might clarify concepts described in the text. Without both, understanding is incomplete. Multimodal RAG systems can retrieve and integrate these different types of data for a holistic response.
    """)

    st.subheader("Applications of Multimodal RAG")
    st.write("""
    - **E-commerce:**  
    Enhance product search by combining visual product images with text descriptions, improving the accuracy of recommendations.

    - **Education:**  
    Support interactive learning by retrieving relevant diagrams, charts, or videos along with textual explanations to help students better understand complex topics.

    - **Customer Support:**  
    Integrate visual aids in support responses, such as including annotated screenshots or diagrams when explaining how to resolve a technical issue.

    """)