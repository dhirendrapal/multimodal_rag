# app/pdf_processing.py
import re
import os
import cv2
import json
import matplotlib.pyplot as plt
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load FAISS index
def load_faiss_index(index_path="data/embeddings/faiss_index"):
    embedding = OpenAIEmbeddings()
    db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    return db


# Query the FAISS index using a language model
def query_faiss(db, query):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer and don't find it in the given context, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain.invoke(query)
    return result


# Extract image references from a given text
def extract_image_references(text):
    pattern = r"\[Image:\s*(.*?)\]"
    return re.findall(pattern, text)


# Display an image using Matplotlib
def display_image(image_path):
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.axis('off')
        plt.show()
    else:
        print(f"Image file {image_path} not found.")


# Main function to handle question-answering and image reference extraction
def ask_question_with_images(question, index_path="data/embeddings/faiss_index", image_folder="extracted_images_new"):
    db = load_faiss_index(index_path)
    result = query_faiss(db, question)

    # Extract answer and page content
    answer = result["result"]
    page_content = result["source_documents"][0].page_content
    page_number = result["source_documents"][0].metadata.get("page", "N/A")
    page_source = os.path.basename(result["source_documents"][0].metadata.get("source"))
    doc_img_src = page_source.split(".")[0]

    save_json(result)

    # Extract and display image references
    image_references = extract_image_references(page_content)
    for image_file in image_references:
        image_path = os.path.join(image_folder, doc_img_src, image_file)
        print(f"Displaying {image_file}...")
        display_image(image_path)

    return answer, page_number, page_source, image_references


def save_json(data, directory="data/responses"):
    def make_serializable(obj):
        """
        Convert non-serializable objects to serializable formats.
        """
        if isinstance(obj, dict):
            return {key: make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(item) for item in obj]
        elif hasattr(obj, "__dict__"):  # For objects with a __dict__ attribute
            return make_serializable(obj.__dict__)
        else:
            return obj  # Return as-is if it is serializable

    # Convert the data to a serializable format
    serializable_data = make_serializable(data)

    # Get all files in the directory
    files = [f for f in os.listdir(directory) if f.startswith("response_") and f.endswith(".json")]

    # Extract numbers from file names
    numbers = []
    for file in files:
        try:
            number = int(file.split('_')[1].split('.')[0])
            numbers.append(number)
        except (IndexError, ValueError):
            continue

    # Determine the next available number
    next_number = max(numbers, default=0) + 1
    filename = f"response_{next_number}.json"

    # Save data to the JSON file
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as json_file:
        json.dump(serializable_data, json_file, indent=4)

