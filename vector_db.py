import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize Chroma client
chroma_client = chromadb.Client(Settings(persist_directory="./chroma_db"))

# Create a collection for user interests
collection = chroma_client.create_collection(name="user_interests")

# Load sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def add_user_interest(user_id, interest):
    vector = sentence_model.encode(interest).tolist()
    collection.add(
        embeddings=[vector],
        documents=[interest],
        metadatas=[{"user_id": str(user_id)}],
        ids=[f"{user_id}_{interest}"]
    )

def get_user_interests(user_id):
    results = collection.get(
        where={"user_id": str(user_id)},
        include=['documents']
    )
    return results['documents'] if results['documents'] else []