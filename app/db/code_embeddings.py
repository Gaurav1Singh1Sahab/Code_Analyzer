from sqlalchemy import Column, Integer, String, ForeignKey
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class CodeEmbedding(Base):

    __tablename__ = "code_embeddings"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    file_path = Column(String)

    chunk_index = Column(Integer)

    code_chunk = Column(String)

    embedding = Column(Vector(384))