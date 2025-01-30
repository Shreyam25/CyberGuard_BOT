# embed_store.py
import chromadb
from sentence_transformers import SentenceTransformer
import spacy
from langchain.llms import GooglePalm
import os
import google.generativeai as genai
<<<<<<< HEAD
import streamlit
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('API_KEY')

=======

import streamlit
>>>>>>> cb8eae51d0efb2cc2d4df5f94877478fbee404d5
# Initialize ChromaDB for vector storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="rag_corpus")

# Load SentenceTransformer model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

# Function to chunk text
def chunk_text(text, chunk_size=300):
    """Splits text into chunks of ~300 words using spaCy."""
    doc = nlp(text)
    chunks, current_chunk = [], ""
    for sent in doc.sents:
        if len(current_chunk) + len(sent.text.split()) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += " " + sent.text
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# Function to embed and store text chunks
def embed_and_store(corpus):
    """Embeds text chunks and stores them in ChromaDB."""
    for i, chunk in enumerate(corpus):
        vector = embedding_model.encode(chunk).tolist()
        collection.add(ids=[str(i)], embeddings=[vector], metadatas=[{"text": chunk}])

def retrieve_top_k(query, k=3):
    """Retrieves top-k most relevant chunks from ChromaDB."""
    query_vector = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_vector], n_results=k)
    return [res["text"] for res in results["metadatas"][0]]

def generate_answer(query, context):
    """Generates an answer using OpenAI GPT with retrieved context."""
    
      # Access the secret key from the environment

      # Please do not use this key in other projects
<<<<<<< HEAD
    genai.configure(api_key=api_key)
=======
    genai.configure(api_key=streamlit.secrets["API"])
>>>>>>> cb8eae51d0efb2cc2d4df5f94877478fbee404d5
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Your name is CyberGuard, a friendly and approachable cybersecurity expert. You are here to help users with any security-related concerns they may have, offering expert guidance and best practices for securing their digital presence. 
    Your goal is to provide accurate, relevant, and easy-to-understand answers based on the context provided. 
    If the context is insufficient, you will offer general cybersecurity best practices that are helpful in a wide range of scenarios. 
    You are knowledgeable, but also approachable, ensuring that users feel comfortable asking questions, whether they are new to cybersecurity or seasoned professionals. 
    
    Always use clear,concise friendly language and encourage users to ask more questions. Your responses should empower users to improve their security with actionable tips.

    Context: {' '.join(context)}

    User Question: {query}
"""


    
    # Generate the completion using the llm object
    # Use generate_text instead of llm()
    response = model.generate_content(prompt)

    
    # Assuming the response structure is: {'choices': [{'message': {'content': 'answer'}}]}
    return response.text 