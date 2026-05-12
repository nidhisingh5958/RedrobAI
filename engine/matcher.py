import math


def cosine_similarity(vec_a, vec_b):
    """Calculate cosine similarity between two sparse vectors."""
    keys = set(vec_a) | set(vec_b)
    dot_product = sum(vec_a.get(key, 0) * vec_b.get(key, 0) for key in keys)
    magnitude_a = math.sqrt(sum(value ** 2 for value in vec_a.values()))
    magnitude_b = math.sqrt(sum(value ** 2 for value in vec_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def rank_candidates(tfidf_vectors, jd_vector):
    """Rank candidates for a single job description vector."""
    ranked_candidates = []

    for candidate_name, tfidf_vector in tfidf_vectors.items():
        score = cosine_similarity(tfidf_vector, jd_vector)
        ranked_candidates.append({
            "name": candidate_name,
            "score": score,
        })

    ranked_candidates.sort(key=lambda item: (-item["score"], item["name"]))

    for index, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = index

    return ranked_candidates[:5]