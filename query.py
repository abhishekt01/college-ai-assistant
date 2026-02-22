import lancedb
from sentence_transformers import SentenceTransformer

# Connect to database
db = lancedb.connect("data")

# Open existing table
table = db.open_table("college_data")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Take user input
query = input("Ask your question: ")

# Convert question to embedding
query_embedding = model.encode(query, normalize_embeddings=True).tolist()

# Search top 3 results
results = table.search(query_embedding).limit(3).to_list()

print("\nTop relevant results:\n")

for r in results:
    print(r["text"])
    print("-----------")