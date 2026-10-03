from document_chunker import create_chunks
from embedding_generator import create_embeddings


chunks = create_chunks("data/knowledge_base.json")

embeddings = create_embeddings(chunks)

print("\n=== ProjectTwin Embeddings ===")
print("Total chunks:", len(chunks))
print("Total embeddings:", len(embeddings))

if len(embeddings) > 0:
    print("Vector size:", len(embeddings[0]))
    print("\nFirst vector:")
    print(embeddings[0])