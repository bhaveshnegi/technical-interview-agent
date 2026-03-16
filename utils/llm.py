from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")

def get_llm():
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3.1-70B-Instruct",
        temperature=0.7
    )
    return llm