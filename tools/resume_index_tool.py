from services.resume_ingestion import load_documents, get_pipeline, get_chroma_vector_store, get_index
import asyncio

async def resume_ingestion_tool():
    # 1. Load Data
    print("Loading documents...")
    documents = load_documents("datas/resumes")
    print("Loaded documents:", len(documents))
    print(documents[0].text[:500])

    # 2. Setup Storing
    print("Initializing vector store...")
    vector_store = get_chroma_vector_store()

    # 3. Ingestion Pipeline
    print("Running ingestion pipeline...")
    pipeline = get_pipeline(vector_store=vector_store)
    await pipeline.arun(documents=documents)

    # 4. Initialize Index
    print("Initializing index...")
    get_index(vector_store)

if __name__ == "__main__":
    asyncio.run(resume_ingestion_tool())