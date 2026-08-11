# Deduplication & Vector Search module initialization

from .exact_dedup import ExactDeduplicationService
from .semantic_dedup import SemanticDeduplicationService
from .embedder import Embedder

__all__ = [
    "ExactDeduplicationService",
    "SemanticDeduplicationService",
    "Embedder"
]
