import sqlite3
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import google.generativeai as genai
import embed_store
from dotenv import load_dotenv
import os
load_dotenv()


api_key = os.getenv('API')

app = Flask(__name__)

# Initialize database
DB_CONFIG = "chat_history.db"  # SQLite database file

# Function to initialize the SQLite database and create a table
def init_db():
    conn = sqlite3.connect(DB_CONFIG)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        role TEXT,
        content TEXT
    )''')
    
    conn.commit()
    conn.close()

# Function to insert a message into the SQLite database
def insert_message(role, content):
    conn = sqlite3.connect(DB_CONFIG)
    cursor = conn.cursor()
    
    # Insert a new message with the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages (timestamp, role, content) VALUES (?, ?, ?)", 
                   (timestamp, role, content))
    
    conn.commit()
    conn.close()

# Flask API endpoint for chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    context = embed_store.retrieve_top_k(query)
    answer = embed_store.generate_answer(query, context)
 
    
    # Store messages in the database
    insert_message("You", query)
    insert_message("CyberGuard", answer)
    
    return jsonify({"answer": answer})

# Flask API endpoint for history
@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect(DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, role, content FROM messages ORDER BY timestamp ASC")
    chat_history = [{"timestamp": str(row[0]), "role": row[1], "content": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(chat_history)

# Flask route to render the chatbot's HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Run the Flask app
if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
