import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.resume_ingestion import build_resume_index
from tools.resume_retriever_tool import query_resume


def main():

    print("Loading resume index...")

    index = build_resume_index()

    while True:

        query = input("\nAsk about the resume: ")

        if query == "exit":
            break

        response = query_resume(index, query)

        print("\nAnswer:")
        print(response)


if __name__ == "__main__":
    main()