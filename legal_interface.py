

import streamlit as st
import requests

# Streamlit UI Setup
st.title("Legal Assistant Chatbot")
st.write("Ask legal questions and get AI-powered responses.")

# Initialize session state variables
if "ai_response" not in st.session_state:
    st.session_state["ai_response"] = ""

if "follow_up_questions" not in st.session_state:
    st.session_state["follow_up_questions"] = []

if "current_follow_up_index" not in st.session_state:
    st.session_state["current_follow_up_index"] = 0  # Track current follow-up question

if "follow_up_answers" not in st.session_state:
    st.session_state["follow_up_answers"] = {}

# Input field for the user question
user_question = st.text_input("Enter your legal question:", "")

if st.button("Ask"):
    if user_question:
        # Reset session state for new query
        st.session_state["ai_response"] = ""
        st.session_state["follow_up_questions"] = []
        st.session_state["follow_up_answers"] = {}
        st.session_state["current_follow_up_index"] = 0

        # Send the user's question to the API
        response = requests.post("http://127.0.0.1:8000/query", json={"question": user_question})

        if response.status_code == 200:
            data = response.json()
            st.session_state["ai_response"] = data.get("ai_response", "No response from AI.")
            st.session_state["follow_up_questions"] = data.get("follow_up_questions", [])
            st.session_state["follow_up_answers"] = {q: "" for q in st.session_state["follow_up_questions"]}
        else:
            st.session_state["ai_response"] = "Error: Unable to retrieve response from AI."

# Display AI response
if st.session_state["ai_response"]:
    st.write("### AI Response:")
    st.write(st.session_state["ai_response"])

# Handle follow-up questions one by one
if st.session_state["follow_up_questions"]:
    st.write("### AI: I need more details before assisting you.")

    current_question = st.session_state["follow_up_questions"][st.session_state["current_follow_up_index"]]
    answer = st.text_input(current_question, value=st.session_state["follow_up_answers"].get(current_question, ""), key="follow_up")

    if st.button("Submit Answer"):
        st.session_state["follow_up_answers"][current_question] = answer

        # Move to the next follow-up question or process answers
        if st.session_state["current_follow_up_index"] < len(st.session_state["follow_up_questions"]) - 1:
            st.session_state["current_follow_up_index"] += 1
        else:
            # Send follow-up answers back to the AI for a final response
            response = requests.post("http://127.0.0.1:8000/process_followups", json={"answers": st.session_state["follow_up_answers"]})
            if response.status_code == 200:
                st.session_state["ai_response"] = response.json().get("ai_response", "No further response from AI.")
            else:
                st.session_state["ai_response"] = "Error processing follow-up answers."

        st.rerun()
