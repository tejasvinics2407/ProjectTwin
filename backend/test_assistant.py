from assistant import ask_project_twin


question = "Which files contain request related functions?"

prompt = ask_project_twin(question)


print("\n=== ProjectTwin Assistant ===")
print("\nGenerated RAG Prompt:")
print(prompt)