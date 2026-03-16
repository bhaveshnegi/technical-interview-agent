def query_resume(index, query):

    retriever = index.as_retriever(similarity_top_k=3)

    nodes = retriever.retrieve(query)

    results = []

    for node in nodes:
        results.append(node.text)

    return "\n\n".join(results)