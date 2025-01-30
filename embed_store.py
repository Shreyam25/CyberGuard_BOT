import chromadb
from sentence_transformers import SentenceTransformer
import spacy
import os
import google.generativeai as genai
import streamlit
from dotenv import load_dotenv


load_dotenv()

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
    genai.configure(api_key=os.getenv("my"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
Your name is CyberGuard, a friendly cybersecurity expert. Provide **concise** responses (maximum 250 words), using **clear, structured, and actionable** advice.

Context: {' '.join(context)}

User Question: {query}

"""




    
    # Generate the completion using the llm object
    # Use generate_text instead of llm()
    response = model.generate_content(prompt)

    return response.text 