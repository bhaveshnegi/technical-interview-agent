from services.resume_ingestion import get_chroma_vector_store, get_index
from tools.resume_analyzer_tool import analyze_resume


def main():

    print("Loading resume index...")

    vector_store = get_chroma_vector_store("vector_store")
    index = get_index(vector_store)

    result = analyze_resume(index)

    print("\n===== Resume Analysis =====\n")

    print("Skills:")
    print(result["skills"])

    print("\nProjects:")
    print(result["projects"])


if __name__ == "__main__":
    main()