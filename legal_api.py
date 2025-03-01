
import sqlite3
import chromadb
import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nltk.corpus import stopwords

# Initialize FastAPI app
app = FastAPI()

# Load stop words
stop_words = set(stopwords.words("english"))

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="C:/Users/sarch/legal_docs/chroma_db")

# Function to preprocess queries (remove stop words)
def preprocess_query(query: str):
    words = query.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Define request model for main question
class QueryRequest(BaseModel):
    question: str
    previous_answers: dict = {}  # Stores answers from follow-up questions
    next_question_index: int = 0  # Tracks which follow-up question to ask next

# Define request model for follow-up responses
class FollowUpRequest(BaseModel):
    question: str
    answer: str
    previous_answers: dict
    next_question_index: int

@app.get("/")
def read_root():
    return {"message": "Legal Assistant API is running!"}

@app.get("/search")
def search(query: str):
    processed_query = preprocess_query(query)

    conn = sqlite3.connect("C:/Users/sarch/legal_docs/legal_assistant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT filename, content, cross_refs FROM legal_docs WHERE content LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()

    return {
        "query": query,
        "processed_query": processed_query,
        "results": [
            {
                "result_number": i + 1,
                "file": row[0],
                "excerpt": row[1][:500],
                "related_documents": row[2].split(", ") if row[2] else None
            }
            for i, row in enumerate(results)
        ]
    }

# Follow-up questions based on topic
FOLLOW_UP_QUESTIONS = {
    "eviction": [
        "Did your landlord provide a formal notice? (e.g., Section 21 or Section 8)",
        "What is the reason for eviction? (e.g., rent arrears, breach of contract, landlord selling)",
        "How much notice have you been given?",
        "Do you have a written tenancy agreement?",
        "Is your landlord following the legal eviction process? (e.g., has a court order)"
    ],
    "employment": [
        "What was the reason given for your dismissal?",
        "Do you have an employment contract?",
        "How long were you employed before being dismissed?",
        "Did your employer follow a disciplinary procedure before dismissing you?",
        "Do you have any written communication regarding your termination?"
    ],
}

@app.post("/query")
def query_legal_docs(request: QueryRequest):
    question = request.question.strip()
    previous_answers = request.previous_answers
    next_question_index = request.next_question_index

    # Identify topic
    topic = None
    if "evict" in question.lower() or "landlord" in question.lower():
        topic = "eviction"
    elif "fired" in question.lower() or "dismissed" in question.lower() or "job loss" in question.lower():
        topic = "employment"

    # If topic is identified and we haven't asked all follow-ups, ask the next one
    if topic and next_question_index < len(FOLLOW_UP_QUESTIONS[topic]):
        return {
            "query": question,
            "ai_response": "I need more details before I can assist you. Please answer the following question:",
            "follow_up_question": FOLLOW_UP_QUESTIONS[topic][next_question_index],
            "next_question_index": next_question_index + 1,
            "previous_answers": previous_answers
        }

    # If all follow-ups are answered, generate a final response
    full_context = f"User Question: {question}\nPrevious Answers: {previous_answers}"

    # Retrieve legal documents
    collection = chroma_client.get_collection(name="legal_docs")
    retrieved_results = collection.query(query_texts=[preprocess_query(question)], n_results=3)

    # Query Mistral AI for legal advice
    ai_response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a legal assistant that provides answers based on UK law."},
            {"role": "user", "content": full_context}
        ]
    )

    return {
        "query": question,
        "ai_response": ai_response["message"]["content"],
        "retrieved_documents": [
            {
                "result_number": i + 1,
                "file": retrieved_results["ids"][0][i],
                "excerpt": retrieved_results["documents"][0][i][:500]
            }
            for i in range(len(retrieved_results["documents"][0]))
        ]
    }

@app.post("/process_followups")
def process_followup(request: FollowUpRequest):
    """Handles follow-up responses and determines next action."""
    question = request.question.strip()
    answer = request.answer.strip()
    previous_answers = request.previous_answers
    next_question_index = request.next_question_index

    # Add the user's answer to stored responses
    previous_answers[question] = answer

    # Identify topic
    topic = None
    if "evict" in question.lower() or "landlord" in question.lower():
        topic = "eviction"
    elif "fired" in question.lower() or "dismissed" in question.lower() or "job loss" in question.lower():
        topic = "employment"

    # If there are more follow-up questions, ask the next one
    if topic and next_question_index < len(FOLLOW_UP_QUESTIONS[topic]):
        return {
            "query": question,
            "ai_response": "Thank you for your response. Please answer the next question:",
            "follow_up_question": FOLLOW_UP_QUESTIONS[topic][next_question_index],
            "next_question_index": next_question_index + 1,
            "previous_answers": previous_answers
        }

    # If all follow-ups are answered, generate a final response
    full_context = f"User Question: {question}\nPrevious Answers: {previous_answers}"

    # Retrieve legal documents
    collection = chroma_client.get_collection(name="legal_docs")
    retrieved_results = collection.query(query_texts=[preprocess_query(question)], n_results=3)

    # Query Mistral AI for final legal advice
    ai_response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a legal assistant that provides answers based on UK law."},
            {"role": "user", "content": full_context}
        ]
    )

    return {
        "query": question,
        "ai_response": ai_response["message"]["content"],
        "retrieved_documents": [
            {
                "result_number": i + 1,
                "file": retrieved_results["ids"][0][i],
                "excerpt": retrieved_results["documents"][0][i][:500]
            }
            for i in range(len(retrieved_results["documents"][0]))
        ]
    }
