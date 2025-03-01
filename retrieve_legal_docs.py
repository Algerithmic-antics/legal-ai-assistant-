
import chromadb
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Paths
DB_PATH = r"C:\Users\sarch\legal_docs\legal_assistant.db"

# Load Sentence Transformer Model
MODEL_PATH = r"C:\Users\sarch\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\fa97f6e7cb1a59073dff9e6b13e2715cf7475ac9"
model = SentenceTransformer(MODEL_PATH)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=r"C:\Users\sarch\legal_docs\chroma_db")
collection = chroma_client.get_collection(name="legal_docs")

def retrieve_legal_info(query, similarity_threshold=0.7, num_results=5):
    """Retrieves the most relevant legal documents based on a query."""
    
    # Generate embedding for the query
    query_embedding = model.encode([query])[0]

    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=num_results
    )

    # Retrieve stored embeddings
    retrieved_embeddings = np.array(results["embeddings"][0])

    # Compute cosine similarity
    query_vector = np.array(query_embedding)
    similarities = np.dot(retrieved_embeddings, query_vector) / (
        np.linalg.norm(retrieved_embeddings, axis=1) * np.linalg.norm(query_vector)
    )

    # Filter results based on similarity threshold
    filtered_results = []
    for i, similarity in enumerate(similarities):
        if similarity >= similarity_threshold:  # Only keep highly relevant results
            filtered_results.append({
                "filename": results["ids"][0][i],
                "excerpt": results["documents"][0][i][:500] + "...",  # First 500 chars
                "similarity": similarity
            })

    # Sort results by similarity score (descending)
    filtered_results = sorted(filtered_results, key=lambda x: x["similarity"], reverse=True)

    # Store retrieval log in SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for result in filtered_results:
        cursor.execute(
            "INSERT INTO retrieval_log (query, filename, timestamp) VALUES (?, ?, ?)",
            (query, result["filename"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    conn.commit()
    conn.close()

    # Display results
    if filtered_results:
        print("\n🔍 **Search Results:**\n")
        for i, res in enumerate(filtered_results):
            print(f"🔹 **Result {i+1}:**")
            print(f"📄 **File:** {res['filename']}")
            print(f"📜 **Excerpt:** {res['excerpt']}")
            print(f"🔹 **Relevance Score:** {res['similarity']:.2f}\n")
            print("-" * 50)
    else:
        print("❌ No highly relevant results found. Try rephrasing your question.")

if __name__ == "__main__":
    user_query = input("\n🔍 Enter a legal question: ")
    retrieve_legal_info(user_query)
