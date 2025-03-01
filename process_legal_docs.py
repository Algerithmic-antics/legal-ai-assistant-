import os
import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

# 🟢 Path to the local model cache (update if needed)
MODEL_PATH = r"C:\Users\sarch\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\fa97f6e7cb1a59073dff9e6b13e2715cf7475ac9"

# 🟢 Path to the folder containing legal documents
LEGAL_DOCS_FOLDER = r"C:\Users\sarch\legal_docs_raw"

# 🟢 Path to SQLite database
DB_PATH = r"C:\Users\sarch\legal_docs\legal_assistant.db"

# 🟢 Load Sentence Transformer Model
try:
    model = SentenceTransformer(MODEL_PATH)
    print("✅ Using locally cached model")
except Exception as e:
    print(f"⚠️ Failed to load model from cache: {e}")
    print("🌐 Downloading model from Hugging Face...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 🟢 Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=r"C:\Users\sarch\legal_docs\chroma_db")

# 🟢 Create or load collection in ChromaDB
collection = chroma_client.get_or_create_collection(name="legal_docs")

def process_and_store_documents():
    """Read text files, generate embeddings, and store them in ChromaDB & SQLite."""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure the database table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS legal_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            content TEXT,
            embedding BLOB
        )
    """)
    
    # Iterate through each text file in the folder
    for filename in os.listdir(LEGAL_DOCS_FOLDER):
        file_path = os.path.join(LEGAL_DOCS_FOLDER, filename)

        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Generate embeddings
        embedding = model.encode([text])[0]  # Convert text to vector

        # Store in SQLite
        cursor.execute("INSERT OR IGNORE INTO legal_docs (filename, content, embedding) VALUES (?, ?, ?)", 
                       (filename, text, embedding.tobytes()))
        
        # Store in ChromaDB
        collection.add(
            ids=[filename],  # Use filename as a unique ID
            documents=[text],
            embeddings=[embedding.tolist()]
        )
        
        print(f"✅ Processed and stored: {filename}")

    # Commit and close database connection
    conn.commit()
    conn.close()
    print("✅ All legal documents processed and stored successfully.")

if __name__ == "__main__":
    process_and_store_documents()
