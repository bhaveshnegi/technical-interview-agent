from llama_index.core import VectorStoreIndex
from services.resume_ingestion import get_chroma_vector_store, get_index

def vector_search(query: str, vector_store_path: str = "vector_store"):
    """
    Performs a semantic search on the candidate's resume to find relevant context.
    
    Args:
        query (str): The search query (e.g., "Tell me about the candidate's internship").
        vector_store_path (str): Path to the persistent chroma vector store.
        
    Returns:
        str: The most relevant context found in the resume.
    """
    try:
        # Load the vector store
        vector_store = get_chroma_vector_store(vector_store_path)
        
        # Get the index
        index = get_index(vector_store)
        
        # Create a query engine
        query_engine = index.as_query_engine(similarity_top_k=2)
        
        # Execute search
        response = query_engine.query(query)
        
        return str(response)
    except Exception as e:
        return f"Error during vector search: {str(e)}"

if __name__ == "__main__":
    # Example usage
    result = vector_search("What are the candidate's key skills?")
    print("Search Result:", result)
