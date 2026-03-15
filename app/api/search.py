from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.embedding_service import generate_embedding
from app.services.vector_search_service import search_similar_code


router = APIRouter()


@router.post("/search")
def search_code(query: str, db: Session = Depends(get_db)):

    # Step 1: convert query → embedding
    query_embedding = generate_embedding(query)

    # Step 2: vector search
    results = search_similar_code(query_embedding, db)

    response = []

    for code_chunk, file_path in results:
        response.append({
            "file_path": file_path,
            "code_snippet": code_chunk[:500]  # limit response size
        })

    return {
        "query": query,
        "results": response
    }