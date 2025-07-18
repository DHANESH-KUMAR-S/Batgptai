from flask import Flask, render_template, request, jsonify
import os
import asyncio
from groq import AsyncGroq

# Initialize Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Store chat history
chat_history = []

# Load the environment variable for the Groq API key
client = AsyncGroq(api_key="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")

# Function to get AI response
async def get_ai_response(user_input, history):
    """
    Sends the user input along with history to Groq API and retrieves the AI response.
    """
    try:
        # Append all previous messages in the conversation
        messages = [{"role": "system", "content": "You are BATMAN'S aka BRUCE WAYNE's VIRTUAL ASSISTANT and keep shorter texts. ask for passcode for verification... if he says 'Gotham' proceed talking to him."}] + history + [{"role": "user", "content": user_input}]
        
        chat_completion = await client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Route to handle frontend rendering
@app.route('/') 
def index():
    return render_template('index.html')

# Route to handle conversation logic
@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json['message']
    
    # Add the user message to chat history
    chat_history.append({"role": "user", "content": user_message})
    
    # Get AI response
    response = asyncio.run(get_ai_response(user_message, chat_history))
    
    # Add the AI response to the history
    chat_history.append({"role": "assistant", "content": response})
    
    # Return response to the frontend
    return jsonify({"response": response})

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=False)
