from retriever import retrieve_documents
from rag import build_prompt


question = "Which files contain request related functions?"

results = retrieve_documents(question, top_k=5)

documents = results["documents"][0]

prompt = build_prompt(question, documents)


print("\n=== ProjectTwin RAG Prompt ===")
print(prompt)