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

uploaded_file = st.file_uploader(
    "Upload yout CV (PDF or TXT)",
    type=["pdf", "txt"]
)

# Job role by input
job_role = st.text_input("Enter the job role you're applying for (optional)")

analyze = st.button("Generate Critique")


def extract_text_from_pdf(file):
    """
    Extract text from a PDF file using PyPDF2.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(file):
    """
    Extract text from a file using its type.
    """
    if file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file.read()))
    else:
        return file.read().decode("utf-8")

if analyze:
    st.write("Generating critique...")
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("Please upload a valid CV file.")
            st.stop()

        prompt = f"""
        You are a helpful assistant that critiques a CV for a job opening. Your goal is to provide a detailed and honest critique of the CV, highlighting areas for improvement and suggesting ways to strengthen the candidate's qualifications. Please provide a comprehensive critique that is both informative and actionable.
        
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience description
        4. Specific improvement for {job_role if job_role else "general job applications"}

        The CV is as follows:
        {file_content}
        
        Please provide a detailed critique of the CV, including a summary of the job role, a description of the candidate's qualifications, and specific areas for improvement. Please also provide suggestions for how the candidate can strengthen their qualifications.
        
        If you are unsure of the answer, please say "I'm not sure" and don't provide a response.
        
        """

        # OpenAI API setup
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                "You are an expert resume reviewer with years of experience "
                "in HR and recruitment."
                    },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        st.markdown(f"### Analysis Results:")
        st.markdown(f"**Job Role:** {job_role if job_role else 'General Job Applications'}")
        st.markdown(f"**Qualifications:** {response.choices[0].message.content}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
