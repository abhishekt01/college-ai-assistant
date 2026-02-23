import lancedb
from sentence_transformers import SentenceTransformer
from scrape import crawl_website


# ------------------ CHUNK FUNCTION ------------------
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


# ------------------ START ------------------

website_url = "https://lbscek.ac.in/"

print("Crawling website...")
pages = crawl_website(website_url, max_pages=150)  # This is now a LIST

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to LanceDB...")
db = lancedb.connect("data")

table = None
chunk_count = 0

print("Creating embeddings and storing...")

for page in pages:

    page_text = page["text"]   # extract actual text from dict

    if not page_text.strip():
        continue

    chunks = chunk_text(page_text)

    for chunk in chunks:

        embedding = model.encode(chunk, normalize_embeddings=True).tolist()

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

        chunk_count += 1
        print(f"Stored chunk {chunk_count}")

print("✅ Website content stored successfully!")