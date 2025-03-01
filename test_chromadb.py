import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=r"C:\Users\sarch\legal_docs\chroma_db")

# Load the legal documents collection
collection = chroma_client.get_collection(name="legal_docs")

# Check how many documents are in ChromaDB
num_docs = collection.count()
print(f"📊 Total Documents in ChromaDB: {num_docs}")

# Retrieve one sample entry
sample_result = collection.peek()
print(f"🔍 Sample Entry: {sample_result}")
