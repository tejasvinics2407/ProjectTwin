from llm import ask_gemini


question = "What is Python?"

answer = ask_gemini(question)


print("\n=== ProjectTwin LLM Test ===")
print("Question:", question)
print("\nGemini Answer:")
print(answer)