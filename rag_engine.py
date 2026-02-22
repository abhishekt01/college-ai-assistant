from dotenv import load_dotenv
load_dotenv()
import requests
import lancedb
from sentence_transformers import SentenceTransformer

# 🔐 PUT YOUR WORKING GEMINI KEY HERE (same one that worked in testgem.py)
import os
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") 

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# ------------------ LOAD DB & MODEL ------------------
db = lancedb.connect("data")
table = db.open_table("college_data")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ MAIN FUNCTION ------------------
def ask_question(question):

    query_embedding = embed_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = table.search(query_embedding).limit(4).to_list()
    context = "\n".join([r["text"] for r in results])

    prompt = f"""
You are a professional college assistant.

Answer clearly in 4-6 complete sentences.
Use ONLY the information provided below.

Context:
{context}

Question:
{question}

Answer:
"""

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(API_URL, json=payload)
    response_json = response.json()

    if "candidates" in response_json:
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response_json}"