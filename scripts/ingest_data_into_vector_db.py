import chromadb
import os
import re

chromadb_client = chromadb.HttpClient(
    os.environ.get("CHROMA_HOST", "http://127.0.0.1:8000")
)
rag_collection = chromadb_client.get_or_create_collection(
    name="rag",
    metadata={"hnsw:space": "cosine"}
)


def get_id_doc_and_metadata_chunks():
    with open("data/processed/context.txt", "r", encoding="utf-8") as f:
        context = f.read()
    chunk_list = context.split("\n\n")
    for i, chunk in enumerate(chunk_list):
        chunk_list[i] = re.sub(" +", " ", chunk_list[i])
        chunk_list[i] = chunk.replace("\n", " ").strip()
    chunk_list = [chunk.strip() for chunk in chunk_list if chunk.strip()]

    id_list = []
    doc_list = []
    metadata_list = []
    for i in range(len(chunk_list)):
        content = chunk_list[i]
        if i >= 1:
            content = f"{chunk_list[i-1]}\n\n{content}"
        if i < len(chunk_list) - 1:
            content = f"{content}\n\n{chunk_list[i+1]}"
        content = content.strip()

        doc_id = str(hash(content))
        id_list.append(doc_id)
        doc_list.append(chunk_list[i])
        metadata_list.append({"content": content})

    return id_list, doc_list, metadata_list


def ingest_documents_into_vector_database():
    print("[VECTOR_DB] Ingesting documents into the vector database...")
    id_list, doc_list, metadata_list = get_id_doc_and_metadata_chunks()
    rag_collection.upsert(
        ids=id_list,
        documents=doc_list,
        metadatas=metadata_list,
    )
    print("[VECTOR_DB] Successfully ingested documents into the vector database.")


if __name__ == "__main__":
    ingest_documents_into_vector_database()
