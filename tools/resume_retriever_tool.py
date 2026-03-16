from services.resume_ingestion import get_index
from utils.llm import get_llm

async def resume_retriever_tool():
    index = await get_index()
    llm = get_llm()

    query_engine = index.as_query_engine(llm=llm)
    
    question = "Analyze the resume and tell me the key skills of Bhavesh Negi."
    print(f"Querying: {question}")
    response = query_engine.query(question)
    
    print("\nResponse:")
    print(response)
