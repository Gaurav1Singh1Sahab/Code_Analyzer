from sqlalchemy.orm import Session

from app.services.parser_service import scan_code_files, chunk_code
from app.services.embedding_service import generate_embedding
from app.db.code_embeddings import CodeEmbedding


def ingest_repository(repo_path: str, project_id: int, db: Session):

    files = scan_code_files(repo_path)

    print(f"Found {len(files)} code files")

    for file_path in files:

        chunks = chunk_code(file_path)

        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(chunk)

            record = CodeEmbedding(
                project_id=project_id,
                file_path=file_path,
                chunk_index=index,
                code_chunk=chunk,
                embedding=embedding
            )

            db.add(record)

    db.commit()

    print("Code ingestion completed")