# Legal AI Assistant - API Documentation

## 📌 Overview
This document provides detailed API usage for the **Legal AI Assistant**, including endpoints for:
- **Legal Queries** (using AI and ChromaDB)
- **Legal Document Retrieval** (from SQLite & ChromaDB)
- **Follow-up Handling**
- **API Health Check**

The API is built using **FastAPI**, and supports local AI processing with Mistral and document retrieval using **ChromaDB** and **SQLite**.

---

## 🚀 Base URL
```
http://127.0.0.1:8000/
```

---

## 📌 Endpoints

### **1️⃣ API Status Check**
Check if the API is running.
```http
GET /
```
✅ **Response:**
```json
{"message": "Legal Assistant API is running!"}
```

---

### **2️⃣ API Health Check** *(New Feature)*
Check if all system components (ChromaDB, SQLite, AI model) are available.
```http
GET /health
```
✅ **Example Response:**
```json
{
  "status": "OK",
  "database": "Connected",
  "chromadb": "Available",
  "ai_model": "Running"
}
```

---

### **3️⃣ Search Legal Documents (ChromaDB & SQLite)**
Retrieve legal documents related to a query.
```http
GET /search?query=<search_term>
```
#### **Example Request:**
```sh
curl "http://127.0.0.1:8000/search?query=Consumer%20Rights%20Act"
```
✅ **Example Response:**
```json
{
  "query": "Consumer Rights Act",
  "processed_query": "consumer rights act",
  "results": [
    {
      "result_number": 1,
      "file": "consumer_rights.txt",
      "excerpt": "Consumer Rights Act 2015 - This Act protects consumers..."
    }
  ]
}
```

---

### **4️⃣ Query Legal Information (AI + Retrieval-Augmented Generation)**
Ask the AI a legal question and retrieve relevant legal documents.
```http
POST /query
```
#### **Example Request:**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:8000/query" -Method Post -Body '{"question": "What are my rights under the Consumer Rights Act?"}' -ContentType "application/json"
```
✅ **Example Response:**
```json
{
  "query": "What are my rights under the Consumer Rights Act?",
  "ai_response": "Under the Consumer Rights Act 2015, consumers have rights regarding faulty goods...",
  "retrieved_documents": [
    {"file": "consumer_rights.txt", "excerpt": "Consumer Rights Act 2015 - This Act protects consumers..."}
  ]
}
```

---

### **5️⃣ Process Follow-Up Questions** *(For step-by-step legal guidance)*
Handle follow-up interactions for more accurate legal responses.
```http
POST /process_followups
```
#### **Example Request:**
```json
{
  "question": "Did your landlord provide a formal notice?",
  "answer": "No",
  "previous_answers": {"question_1": "Yes"},
  "next_question_index": 2
}
```
✅ **Example Response:**
```json
{
  "query": "Did your landlord provide a formal notice?",
  "ai_response": "Thank you for your response. Please answer the next question:",
  "follow_up_question": "What is the reason for eviction? (e.g., rent arrears, breach of contract, landlord selling)",
  "next_question_index": 3,
  "previous_answers": {"question_1": "Yes", "question_2": "No"}
}
```

---

## 📌 Error Handling
| Error Code | Meaning | Possible Fix |
|------------|---------|--------------|
| `404 Not Found` | Endpoint does not exist | Check the endpoint URL in `/docs`. |
| `422 Unprocessable Entity` | Incorrect request format | Ensure JSON body is correctly structured. |
| `500 Internal Server Error` | Server crash | Restart the API, check logs for errors. |

---

## 📌 Testing the API
### **1️⃣ Using cURL**
```sh
curl "http://127.0.0.1:8000/search?query=landlord"
```

### **2️⃣ Using Postman**
- Open Postman
- Select **POST** and enter `http://127.0.0.1:8000/query`
- Add JSON body:
  ```json
  {"question": "What are my rights under the Consumer Rights Act?"}
  ```
- Click **Send**

### **3️⃣ Using Python Requests**
```python
import requests

url = "http://127.0.0.1:8000/query"
data = {"question": "What are my rights under the Consumer Rights Act?"}
response = requests.post(url, json=data)
print(response.json())
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📧 Contact & Support
For issues, open a GitHub Issue or contact the project owner.
📌 **GitHub Repo:** [Legal AI Assistant](https://github.com/Algerithmic-antics/legal-ai-assistant)

