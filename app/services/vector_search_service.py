from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.code_embeddings import CodeEmbedding


def search_similar_code(query_embedding, db, limit=5):

    sql = text("""
    SELECT code_chunk, file_path
    FROM code_embeddings
    ORDER BY embedding <=> CAST(:embedding AS vector)
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