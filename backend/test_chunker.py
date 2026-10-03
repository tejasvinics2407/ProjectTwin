from document_chunker import create_chunks


chunks = create_chunks("data/knowledge_base.json")

print("\n=== ProjectTwin Document Chunks ===")
print("Total chunks:", len(chunks))

if chunks:
    print("\nFirst chunk:")
    print(chunks[0])