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

    # 🧠 Prompt (same as yours)
    prompt = f"""
You are [Mithra], a multilingual voice assistant built by Abhishek T (CSE Batch 2022-2026, LBS College of Engineering, Kasaragod, Kerala) for an AI college project.

Your responsibilities:
- Answer all college-related questions clearly and accurately.
- Provide complete and helpful responses.
- Maintain a polite, humble, and professional tone.
- Sound natural and human-like in your responses.

Language Rules:
- If the user asks in English, respond in English.
- If the user asks in Malayalam, respond fully in Malayalam.

ownership:
- When asked who built you, who owns you, your creators, or similar: Always respond exactly: "I was built by Abhishek T(CSE Batch 2022-2026, LBS College of Engineering, Kasaragod, Kerala) for an AI college project."

Context:
{context}

Question:
{question}

Answer:"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-small-online",  # ✅ FIXED: Use correct model name
        "messages": [{"role": "user", "content": prompt}],  # ✅ Simplified
        "temperature": 0.3,
        "max_tokens": 1000  # ✅ Added
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=30)
        
        # ✅ DEBUG: Print raw response
        st.write("**Debug:** Status:", response.status_code)
        st.write("**Debug:** Response preview:", response.text[:200])
        
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text[:100]}"
            
        response_json = response.json()
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            return f"❌ Unexpected format: {response_json}"
            
    except requests.exceptions.Timeout:
        return "❌ API timeout - please try again"
    except requests.exceptions.JSONDecodeError as e:
        return f"❌ Invalid JSON: {response.text[:200]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
