from retriever import retrieve_documents


query = "Which files contain request related functions?"

results = retrieve_documents(query, top_k=5)


print("\n=== ProjectTwin Retriever ===")
print("Query:", query)

print("\nRelevant files:")

for file_name in results["documents"][0]:
    print("-", file_name)