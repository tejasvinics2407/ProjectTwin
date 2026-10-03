from retriever import retrieve_documents
from rag import build_prompt


def ask_project_twin(question):

    # Step 1: Find relevant project information
    results = retrieve_documents(question, top_k=5)

    # Step 2: Get the retrieved documents
    documents = results["documents"][0]

    # Step 3: Build the RAG prompt
    prompt = build_prompt(question, documents)

    return prompt