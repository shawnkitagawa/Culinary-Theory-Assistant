from app.database.db import Chunk


def get_context_text(results: list[tuple[Chunk, str, float]]) -> str:
    contexts = []

    for chunk, document_title, distance_score in results:
        contexts.append(
            f"[Source: {document_title}, Pages {chunk.page_start}-{chunk.page_end}, "
            f"Distance: {distance_score:.3f}]\n"
            f"{chunk.chunk_text}"
        )

    return "\n\n---\n\n".join(contexts)