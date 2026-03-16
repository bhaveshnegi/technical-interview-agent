from graphs.interview_graph import build_graph
from services.resume_ingestion import get_chroma_vector_store, get_index

def main():

    print("Loading existing resume index...")

    vector_store = get_chroma_vector_store("vector_store")

    index = get_index(vector_store)

    graph = build_graph()

    state = {
        "resume_text": "",
        "skills": [],
        "projects": [],
        "question_list": [],
        "current_question": None,
        "candidate_answer": None,
        "score": None,
        "feedback": None,
        "conversation_history": [],
        "question_index": 0,
        "interview_complete": False,
        "resume_index": index
    }

    graph.invoke(state)


if __name__ == "__main__":
    main()