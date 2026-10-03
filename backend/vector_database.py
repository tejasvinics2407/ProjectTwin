import chromadb


client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="project_twin"
)


def store_embeddings(chunks, embeddings):
    ids = []
    documents = []

    for index, chunk in enumerate(chunks):
        ids.append(str(index))

        content = chunk["content"]

        document = (
            f"File: {chunk['file']}\n"
            f"Imports: {content['imports']}\n"
            f"Functions: {content['functions']}\n"
            f"Classes: {content['classes']}"
        )

        documents.append(document)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist()
    )

    print(f"Stored {len(chunks)} embeddings in ChromaDB.")