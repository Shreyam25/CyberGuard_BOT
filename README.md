## CyberGuard Chatbot with RAG

## Overview
CyberGuard is a chatbot using Retrieval-Augmented Generation (RAG) to answer queries based on data scraped from Wikipedia. The backend is powered by Flask, ChromaDB for vector storage, and Google Generative AI for response generation. It saves chat history in an SQLite database (`chat_history.db`).

---

## Installation & Setup

### 1. Clone the Repository

      git clone https://github.com/Shreyam25/CyberGuard_BOT.git
      cd CyberGuard_Chatbot

### 2. Set up Virtual Environment
      python -m venv venv
      source venv/bin/activate  

### 3. Install Dependencies
      pip install -r requirements.txt
   
### 4. Setting Up SQLite Database :
The project uses SQLite3 to store chat history. To set up the database-
    
          init_db()
This will create a chat_history.db SQLite file if it doesn’t already exist. The database will contain the messages table with columns id, timestamp, role, and content.

### 5. Environment Variables
Create a .env file and add the following:
    
          API=<Your Google Generative AI API Key>
    
### 6. Running the Application
To start the Flask app locally:
        python rag_chatbot.py
The app will run on http://127.0.0.1:5000/.
