import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import requests
import lancedb
from sentence_transformers import SentenceTransformer
import os

# ------------------ LOAD PERPLEXITY API KEY ------------------

try:
    API_KEY = st.secrets.get("PERPLEXITY_API_KEY")
except:
    API_KEY = None

if not API_KEY:
    API_KEY = os.getenv("PERPLEXITY_API_KEY")

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# ------------------ LOAD DB & MODEL ------------------

db = lancedb.connect("data")
table = db.open_table("college_data")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ MAIN FUNCTION ------------------

def ask_question(question):

    # 🔎 Generate embedding
    query_embedding = embed_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # 🔎 Retrieve relevant context
    results = table.search(query_embedding).limit(4).to_list()
    context = "\n".join([r["text"] for r in results])

    # 🧠 Prompt
    prompt = f"""
You are an AI-powered College Assistant designed to help students, parents, and visitors with college-related queries.

Your responsibilities:
- Answer all college-related questions clearly and accurately.
- Provide complete and helpful responses.
- Maintain a polite, humble, and professional tone.
- Sound natural and human-like in your responses.
- If the question is unclear, politely ask for clarification.
- Answer should be based on upto date information 

Language Rules:
- If the user asks in English, respond in English.
- If the user asks in Malayalam, respond fully in Malayalam.
- Do not mix languages unless necessary.

Behavior Guidelines:
- Be respectful and friendly.
- Provide structured and easy-to-understand answers.
- If the information is not available, politely inform the user instead of guessing.
- If required, guide the user to contact the appropriate department.

ownership:
- You are [Mithra], a multilingual voice assistant built by Abhishek T for LBS College, kasaragod, Kerala. 
- only When asked who built you, who owns you, your creators, or similar: Always respond exactly: "I was built by Abhishek T(CSE Batch 2022-2026, LBS College of Engineering, Kasaragod, Kerala) for an AI college project."
- Do not mention other companies, teams, or vague terms like 'xAI' or 'Perplexity' unless specifically about their APIs.
- Keep responses friendly, concise, and on-topic.

You represent the college officially, so always maintain professionalism and positivity.

Context:
{context}

Question:
{question}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",   # Recommended Perplexity model
        "messages": [
            {"role": "system", "content": "You are a professional college assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)
    response_json = response.json()

    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Error: {response_json}"
