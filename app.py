import os
import streamlit as st
import shutil
from PIL import Image
from lyzr import ChatBot
import time

os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.set_page_config(
    page_title="Lyzr Contract Analyzer💼",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar .sidebar-content {
        background-color: #333333;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        margin: 10px 0;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .st-expander {
        border: 2px solid #007BFF;
        border-radius: 10px;
        padding: 10px;
    }
    .st-expander>summary {
        font-size: 1.2em;
        font-weight: bold;
        color: #007BFF;
    }
    .stFileUploader>label {
        font-size: 1.1em;
        font-weight: bold;
        color: #000000;
    }
    .stMarkdown {
        font-size: 1.1em;
        color: #333333;
    }
    .stImage>img {
        margin-bottom: 20px;
    }
    .stAlert {
        background-color: #e9f5ff;
        border-left: 5px solid #007BFF;
        color: #333333;
    }
    .loading-text {
        font-size: 1.2em;
        color: #007BFF;
        font-weight: bold;
    }
    .sidebar .sidebar-content a {
        color: #ffffff;
    }
    .stSidebar {
        background-color: #333333;
        color: #ffffff;
        font-size: 1.1em;
        font-weight: bold;
        padding: 10px;
    }
    .main h1, .main h2, .main h3 {
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Contract Analyzer💼")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown(
    """
    Welcome to our Contract Analyzer app! Simply upload your contracts, and we'll provide you with:
    - **Clear risk insights**
    - **Easy-to-understand explanations**
    - **Practical suggestions** to help you get the best out of your agreements.
    """
)

# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)


# File upload widget
uploaded_file = st.file_uploader("Choose a Word file (.docx)", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded Word file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved at {file_path}")

    def get_files_in_directory(directory="data"):
        files_list = []
        if os.path.exists(directory) and os.path.isdir(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    files_list.append(file_path)
        return files_list

    def rag_implementation():
        path = get_files_in_directory()
        path = path[0]
        rag = ChatBot.docx_chat(
            input_files=[str(path)],
            llm_params={"model": "gpt-4-turbo-preview"},
        )
        return rag

    def resume_response():
        rag = rag_implementation()
        prompt = """  
        You are an expert CONTRACT LAWYER and LEGAL CONSULTANT. Your task is to SCRUTINIZE the user-uploaded document and DELIVER a comprehensive analysis.
        Please follow these steps for a thorough examination:
        1. INITIATE your review on the user's document by IDENTIFYING RISKS, focusing on highlighting potentially risky clauses such as INDEMNITY CLAUSES, TERMINATION CONDITIONS, PAYMENT TERMS, and LIABILITY LIMITATIONS.
        2. PROVIDE DETAILED EXPLANATIONS for each identified risk and clause, ensuring that the user understands the implications of these terms within the contract.
        3. DEVELOP and SUGGEST possible REVISIONS or MITIGATIONS for the identified risks to protect the user's interests effectively.
        Remember, You MUST present actionable advice that can be applied directly to improve the contract in question.
        """
        response = rag.chat(prompt)
        return response.response

    with st.spinner('Analyzing the contract... Please wait.'):
        time.sleep(2)  # Simulate the delay for analysis
        analysis_result = resume_response()
        st.success("Analysis complete!")
        st.markdown("### Analysis Result")
        st.markdown(analysis_result)

# Add a sidebar with useful links
st.sidebar.title("Contact Us")
st.sidebar.markdown(
    """
    - [Lyzr](https://www.lyzr.ai/)
    - [Book a Demo](https://www.lyzr.ai/book-demo/)
    - [Discord](https://discord.gg/nm7zSyEFA2)
    - [Slack](https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw)
    """
)
