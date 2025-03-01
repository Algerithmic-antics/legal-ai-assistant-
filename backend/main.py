import babyagi
import os

# Set up BabyAGI with a web dashboard
app = babyagi.create_app('/dashboard')

# ✅ Replace OpenAI with Ollama (DeepSeek-Legal)
babyagi.add_key_wrapper('ollama_model', 'deepseek-legal')  # Change to 'mistral' if needed

# ✅ Define a function to send queries to Ollama
import requests

def ask_ollama(query):
    """Send a query to the local Ollama model and return the response."""
    response = requests.post(
        "http://localhost:11434/api/generate",  # Ollama's local API
        json={"model": "deepseek-legal", "prompt": query}
    )
    return response.json().get("response", "No response from Ollama.")

# ✅ Route to test Ollama
@app.route('/ask/<query>')
def ask(query):
    return ask_ollama(query)

@app.route('/')
def home():
    return f"Welcome to the main app. Visit <a href=\"/dashboard\">/dashboard</a> for BabyAGI dashboard."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
