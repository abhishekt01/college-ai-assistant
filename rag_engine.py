def ask_question(question):
    if not API_KEY:
        return "❌ No Perplexity API key found. Please add PERPLEXITY_API_KEY to .env or Streamlit secrets."
    
    # 🔎 Generate embedding & context (same as before)
    query_embedding = embed_model.encode(question, normalize_embeddings=True).tolist()
    results = table.search(query_embedding).limit(4).to_list()
    context = "\n".join([r["text"] for r in results])

    # 🧠 Clean, working prompt
    prompt = f"""You are [Mithra], a multilingual voice assistant built by Abhishek T (CSE Batch 2022-2026, LBS College of Engineering, Kasaragod, Kerala) for an AI college project.

Answer this college question using ONLY the provided context:

CONTEXT:
{context}

QUESTION: {question}

Answer concisely and naturally:"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"  # ✅ FIX: Prevents bot detection
    }

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",  # ✅ CORRECT Perplexity model (sonar-pro doesn't exist)
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=30)
        
        # ✅ CRITICAL: Check raw response FIRST (before any .json())
        st.info(f"🔍 Status: {response.status_code}")
        st.info(f"🔍 Response preview: {response.text[:300]}...")
        
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}\n{response.text[:200]}"
        
        # ✅ Only parse JSON if status is 200 AND response has content
        if not response.text.strip():
            return "❌ Empty response from API"
            
        response_json = response.json()
        
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return f"❌ Unexpected format: {response_json}"
            
    except requests.exceptions.Timeout:
        return "⏰ API timeout - try again"
    except Exception as e:
        return f"❌ Error: {str(e)}\nResponse: {response.text[:200] if 'response' in locals() else 'No response'}"
