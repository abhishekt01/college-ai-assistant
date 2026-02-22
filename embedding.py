# Import LanceDB to store data
import lancedb

# Import sentence-transformers instead of OpenAI
from sentence_transformers import SentenceTransformer

# Import our crawler function from scrape.py
from scrape import crawl_website

# Function to split big text into smaller pieces
def chunk_text(text, chunk_size=500):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# 🔴 Change this to your real college website
website_url = "https://lbscek.ac.in/"

# Crawl website and get all text
print("Crawling website...")
website_text = crawl_website(website_url, max_pages=30)

# Split text into chunks
print("Splitting into chunks...")
chunks = chunk_text(website_text)

# Load embedding model ONCE (important)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to database (creates folder named data)
db = lancedb.connect("data")

# Variable to track if table is created
table = None

print("Creating embeddings and storing...")

for chunk in chunks:

    # Create embedding vector from text (LOCAL, no API)
    embedding = model.encode(chunk, normalize_embeddings=True).tolist()

    # If table doesn't exist yet, create it with first row
    if table is None:
        table = db.create_table(
            "college_data",
            data=[{
                "text": chunk,
                "vector": embedding
            }],
            mode="overwrite"
        )
    else:
        table.add([{
            "text": chunk,
            "vector": embedding
        }])

print("✅ Website content stored successfully!")