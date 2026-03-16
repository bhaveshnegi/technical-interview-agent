import chromadb

from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext


def build_resume_index():

    # Load PDF resumes
    documents = SimpleDirectoryReader("../datas/resumes").load_data()

    # HuggingFace embedding model
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Chroma client
    chroma_client = chromadb.PersistentClient(path="./vector_store")

    chroma_collection = chroma_client.get_or_create_collection(
        name="resume_collection"
    )

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    # Build index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

    return index