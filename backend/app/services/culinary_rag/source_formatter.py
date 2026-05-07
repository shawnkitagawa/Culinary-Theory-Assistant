from app.database.db import Chunk


def format_sources(results: list[tuple[Chunk, str, float]]) -> list[dict]:
    return [
        {
            "chunk_id": str(chunk.chunk_id),
            "document_title": document_title,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "distance": distance_score,
            "similarity": 1 - distance_score,
        }
        for chunk, document_title, distance_score in results
    ]