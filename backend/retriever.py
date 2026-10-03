from sentence_transformers import SentenceTransformer
from vector_database import collection


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query, top_k=5):

    # Convert the user's question into an embedding
    query_embedding = model.encode(query)

    # Search ChromaDB for similar documents
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results