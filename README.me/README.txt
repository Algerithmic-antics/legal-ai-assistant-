# Legal AI Assistant

## 📌 Overview

The **Legal AI Assistant** is a mobile-ready AI-powered assistant designed to provide:

- **Legal Advice** based on UK laws.
- **Legal Document Retrieval** from ChromaDB and SQLite.
- **Letter Writing Assistance** for complaints and legal notices.
- **Voice-to-Voice Legal Assistance** (Planned feature).

The system is powered by **FastAPI**, **ChromaDB**, and **SQLite**, and supports **local AI inference** with optional cloud scaling.

---

## 📢 About the Project

The Legal AI Assistant is designed to assist individuals in navigating legal issues by:

- Providing AI-generated legal advice based on UK laws.
- Writing letters (e.g., complaints, appeals) on behalf of users.
- Engaging in voice-to-voice interactions, allowing users to have real-time legal discussions.
- Using Retrieval-Augmented Generation (RAG) with ChromaDB to fetch relevant legal documents.
- Running locally first with offline AI models, with a future option to scale via cloud.

🚀 **Project Repository:** [GitHub](https://github.com/Algerithmic-antics/legal-ai-assistant)

---

## 📂 Project Structure

```plaintext
legal-ai-assistant/
│── backend/  # Backend logic and AI processing
│   ├── chromadb/  # Stores embeddings for RAG-based legal document retrieval
│   ├── test/  # Unit and integration tests for backend components
│   ├── legal_api.py  # FastAPI-based API handling user queries
│   ├── process_legal_docs.py  # Processes and indexes legal documents into ChromaDB
│   ├── retrieve_legal_docs.py  # Retrieves legal data based on user queries
│   ├── scrape_legal_docs.py  # Web scrapers for legal websites
│   ├── test_chromadb.py  # Tests legal document retrieval
│   ├── requirements.txt  # Python dependencies
│   ├── pyproject.toml  # Project metadata (Poetry-based)
│   ├── poetry.lock  # Dependency lock file
│
│── frontend/  # User interface and interaction handling
│   ├── static/  # Static files (CSS, JS)
│   ├── legal_interface.py  # Chatbot interface (Streamlit)
│
│── legal_ai_assistant/  # Main package containing core business logic
│   ├── setup.py  # Python package setup file
│
│── docs/  # Documentation files
│   ├── README.md  # This file (Project documentation)
│
│── LICENSE  # License file
│── main.py  # Main entry point
```

---

## ⚙️ Features

✅ **AI-Powered Legal Advice**

- Users can ask legal questions, and the assistant provides responses based on UK legal documents.

✅ **Legal Document Retrieval (RAG)**

- The AI searches ChromaDB for relevant UK legislation, case law, and legal precedents.

✅ **Letter Writing Assistance**

- The AI can draft formal complaint letters, appeals, legal notices, and more.

✅ **Voice-to-Voice Legal Assistant (Planned Feature)**

- Users will interact via speech with the AI for legal queries.

✅ **Local & Cloud Model Support**

- **Local Mode:** Runs on Mistral 7B (DeepSeek offline).
- **Cloud Mode:** Future upgrade to DeepSeek 30B+ for complex queries.

✅ **Scalable Architecture**

- Uses **FastAPI** for the backend API.
- **Flutter or React Native** planned for the mobile app.
- **SQLite** stores structured legal information.
- **ChromaDB** manages vector embeddings for legal retrieval.

---

## 🚀 Installation & Setup

### **1️⃣ Prerequisites**

Ensure you have the following installed:

- **Python 3.9+**
- **FastAPI & Uvicorn**
- **ChromaDB** (for document retrieval)
- **SQLite** (for structured legal data storage)

### **2️⃣ Clone the Repository**

```sh
git clone https://github.com/Algerithmic-antics/legal-ai-assistant.git
cd legal-ai-assistant
```

### **3️⃣ Install Dependencies**

Using **Poetry**:

```sh
poetry install
```

Or using **pip**:

```sh
pip install -r requirements.txt
```

### **4️⃣ Start the API Server**

Run the FastAPI server:

```sh
uvicorn legal_api:app --host 0.0.0.0 --port 8000 --reload
```

Check if it's running:

```sh
curl http://127.0.0.1:8000/
```

✅ Expected output:

```json
{"message": "Legal Assistant API is running!"}
```

---

## 📅 Roadmap

🚀 **Phase 1 (Current) - Backend AI & RAG System** ✅ Implement FastAPI + SQLite + ChromaDB ✅ Develop AI-powered legal question-answering system ✅ Improve retrieval-augmented generation (RAG) model

🔜 **Phase 2 - UI & Mobile App** 🔹 Develop **Flutter/React Native** mobile app 🔹 Build **real-time speech-to-text & text-to-speech features**

🔜 **Phase 3 - Cloud Scaling** 🔹 Upgrade to **DeepSeek-LLM 30B (Cloud-Based)** for complex legal analysis 🔹 Introduce **user accounts & case tracking**

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 📧 Contact & Support

For issues, open a GitHub Issue or contact the project owner. 📌 **GitHub Repo:** [Legal AI Assistant](https://github.com/Algerithmic-antics/legal-ai-assistant)

