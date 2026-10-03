from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    texts = []

    for chunk in chunks:
        file_name = chunk["file"]
        content = chunk["content"]

        text = (
            f"File: {file_name}\n"
            f"Imports: {content['imports']}\n"
            f"Functions: {content['functions']}\n"
            f"Classes: {content['classes']}"
        )

        texts.append(text)

    embeddings = model.encode(texts)

    return embeddings