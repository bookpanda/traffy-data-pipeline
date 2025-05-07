import os
from qdrant_client.http.models import SearchRequest
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import numpy as np

coord_min=np.array([3.74644, 0.46217])
coord_max=np.array([14.13452, 100.93493])

def transform_coordinate(coord, coord_min=coord_min, coord_max=coord_max):
    coord_np = np.array(coord)  # Convert to numpy array

    # Normalize the single coordinate
    normalized_coord = (coord_np - coord_min) / (coord_max - coord_min + 1e-8)

    return normalized_coord


def preprocess_text(t, max_char_len=100):
    t = t.strip()
    return t[:max_char_len] # truncate long ones

# Load variables from .env into the environment
load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Connect to Qdrant Cloud
client = QdrantClient(
    url=f"https://{QDRANT_HOST}",
    api_key=QDRANT_API_KEY,
)

# I don't know why it not work in my env, so i download it
# model = SentenceTransformer('kornwtp/ConGen-simcse-model-roberta-base-thai')
model = SentenceTransformer('./local_model')

def find_org(comment, coord, type):
    text = preprocess_text(comment)
    coord = transform_coordinate(coord)
    type = np.array(type)/100
    text_vec = model.encode(text)
    text_vec = text_vec/100*np.linalg.norm(text_vec)
    query_vector = np.hstack([text_vec, coord, type])
    print(text,coord)
    result = client.search(
        collection_name="dsde_project2",
        query_vector=query_vector,
        limit=5,  # top 5 results
        with_payload=True
    )
    organize = [point.payload.get("organization") for point in result]
    return organize