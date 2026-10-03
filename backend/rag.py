def build_prompt(question, retrieved_documents):

    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are ProjectTwin, an AI assistant that understands software projects.

Answer the user's question using the project information provided below.

PROJECT INFORMATION:
{context}

USER QUESTION:
{question}

Give a clear and concise answer based only on the project information.
"""

    return prompt