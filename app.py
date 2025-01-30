import streamlit as st
import sqlite3
from datetime import datetime
from langchain.llms import GooglePalm
import google.generativeai as genai
from embed_store import retrieve_top_k, generate_answer

# Initialize SQLite database
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

# Streamlit page configuration
st.set_page_config(page_title="Chat with CyberGuard", page_icon="🤖")

# Title of the Streamlit page
st.title("CyberGuard")
st.markdown("""
    ## Hello, I am CyberGuard!

    I am an intelligent RAG-based chatbot designed to solve your cybercrime and cybersecurity-related doubts within seconds. With access to vast databases and real-time threat intelligence, I provide accurate and quick responses to help you stay safe online.

    Ask me anything about cybersecurity, and I’ll guide you through potential threats, solutions, and best practices to protect your digital assets.
""")
# Function to display chat history from the SQLite database
def display_history():
    conn = sqlite3.connect(DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, role, content FROM messages ORDER BY timestamp ASC")
    chat_history = cursor.fetchall()
    conn.close()
    
    for msg in chat_history:
        st.write(f"**{msg[0]} - {msg[1]}**: {msg[2]}")

# Function to handle AI query and return answer
def get_chat_answer(query):
    context = retrieve_top_k(query)
    answer = generate_answer(query, context)
    
    return answer

# Initialize database (if not already done)
init_db()

# User input for chat
query = st.text_input("Ask me anything:")

if query:
    # Get the answer from the AI model
    answer, context = get_chat_answer(query)
    
    # Display the answer and context
    st.write("**Answer:**", answer)
    
    # Store user and system messages in the SQLite database
    insert_message("user", query)
    insert_message("system", answer)
    
    # Display the updated chat history
    st.write("### Chat History")
    display_history()
