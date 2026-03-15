from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.code_embeddings import CodeEmbedding


def search_similar_code(query_embedding, db: Session, limit: int = 5):

    sql = text("""
    SELECT content, file_path
    FROM code_embeddings
    ORDER BY embedding <=> :embedding
    LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": query_embedding,
            "limit": limit
        }
    )

    return result.fetchall()