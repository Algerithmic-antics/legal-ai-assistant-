import sqlite3

# Connect to the database
conn = sqlite3.connect("C:/Users/sarch/legal_docs/legal_assistant.db")
cursor = conn.cursor()

# Check if the table 'legal_docs' exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='legal_docs';")
table_exists = cursor.fetchone()

if table_exists:
    print("✅ Table 'legal_docs' exists.")

    # Fetch the column structure
    cursor.execute("PRAGMA table_info(legal_docs);")
    columns = cursor.fetchall()

    if columns:
        print("\n📂 Columns in 'legal_docs':")
        for column in columns:
            print(column)
    else:
        print("⚠️ No columns found in 'legal_docs'.")
else:
    print("❌ Table 'legal_docs' does NOT exist.")

conn.close()
