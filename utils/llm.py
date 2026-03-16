from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():

    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
        temperature=0.3,
        max_new_tokens=50,
        huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    )

    chat_model = ChatHuggingFace(llm=llm)

    return chat_model