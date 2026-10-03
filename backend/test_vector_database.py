from document_chunker import create_chunks
from embedding_generator import create_embeddings
from vector_database import store_embeddings


# Load project chunks
chunks = create_chunks("data/knowledge_base.json")

# Create embeddings
embeddings = create_embeddings(chunks)

# Store embeddings in ChromaDB
store_embeddings(chunks, embeddings)

print("\n=== ProjectTwin Vector Database ===")
print("Vector database setup complete!")