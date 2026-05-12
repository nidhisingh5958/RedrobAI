app.py
from engine import (
    SKILL_ALIASES,
    cosine_similarity,
    rank_candidates,
    normalize_skills,
    deduplicate_skills,
    compute_tfidf
)