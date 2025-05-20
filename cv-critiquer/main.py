import streamlit as st
import PyPDF2
import os
import io
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Set up Streamlit UI
st.set_page_config(
    page_title="AI CV Critiquer",
    page_icon="📄",
    layout="centered"
)

# Set up Streamlit components
st.title("AI CV Critiquer")


with st.form("form"):
    st.markdown(
        """
    # CV Critiquer
    
    This tool allows you to critique a CV and get a score for each section. It uses OpenAI's GPT-3 model to generate a critique for each section.
    
    ## How to use
    
    1. Upload your CV as a PDF file.
    2. Click the "Generate Critique" button.
    3. Review the critique and provide feedback.
    4. Click the "Submit" button to submit your feedback.
    5. Wait for the system to generate a new critique.
    6. Repeat steps 2-5 until you are satisfied with the critique.
    7. Click the "Download" button to download the final critique as a PDF file.
    
        """,
        unsafe_allow_html=True,
    )

    # Upload CV

# OpenAI API setup

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader(
    "Upload yout CV (PDF or TXT)",
    type=["pdf", "txt"]
)

job_role = st.text_input("Enter the job role you're applying for (optional)")

analyze = st.button("Generate Critique")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file.read()))
    else:
        return file.read().decode("utf-8")

