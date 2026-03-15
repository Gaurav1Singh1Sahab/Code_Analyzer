from sentence_transformers import SentenceTransformer

# load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Convert text to embedding vector
    """
    embedding = model.encode(text)

    return embedding.tolist()