from services.resume_ingestion import get_index
from utils.llm import get_llm

def resume_retriever_tool(index, query):

    retriever = index.as_retriever(similarity_top_k=3)

    nodes = retriever.retrieve(query)

    results = []

    for node in nodes:
        results.append(node.text)

    return "\n\n".join(results)
