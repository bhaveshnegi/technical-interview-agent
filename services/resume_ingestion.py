from llama_index.core import SimpleDirectoryReader

from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.ingestion import IngestionPipeline

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def load_documents(directory):
    reader = SimpleDirectoryReader(input_dir=directory)
    return reader.load_data()

def get_pipeline(vector_store=None):
    return IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
            HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        ],
        vector_store=vector_store,
    )

def get_chroma_vector_store(path="./vector_store", collection_name="resume_collection"):
    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)

def get_index(vector_store, embed_model_name="BAAI/bge-small-en-v1.5"):
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    return VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)