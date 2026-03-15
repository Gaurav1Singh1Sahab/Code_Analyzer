from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.embedding_service import generate_embedding
from app.services.vector_search_service import search_similar_code

from app.services.llm_service import generate_code_explanation


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


@router.post("/ask")
def ask_codebase(query: str, db: Session = Depends(get_db)):

    # generate query embedding
    query_embedding = generate_embedding(query)

    # vector search
    results = search_similar_code(query_embedding, db)

    snippets = []
    sources = []

    for code_chunk, file_path in results:
        snippets.append(code_chunk[:1500])
        sources.append(file_path)

    # LLM reasoning
    explanation = generate_code_explanation(query, snippets)

    return {
        "question": query,
        "answer": explanation,
        "sources": sources
    }