engine/matcher.py
import math

def cosinesimilarity(veca, vec_b):
    """
    Calculate the cosine similarity between two vectors.
    
    Args:
    vec_a (dict): First vector.
    vec_b (dict): Second vector.
    
    Returns:
    float: Cosine similarity between the two vectors.
    """
    # Calculate the dot product
    dotproduct = sum(veca.get(skill, 0) * vecb.get(skill, 0) for skill in set(veca) | set(vec_b))
    
    # Calculate the magnitude of each vector
    magnitudea = math.sqrt(sum(val  2 for val in veca.values()))
    magnitudeb = math.sqrt(sum(val  2 for val in vecb.values()))
    
    # Check for division by zero
    if magnitudea == 0 or magnitudeb == 0:
        return 0
    
    # Calculate the cosine similarity
    return dotproduct / (magnitudea * magnitude_b)

def rankcandidates(tfidfvectors, jd_vector):
    """
    Rank candidates based on their TF-IDF vectors and a job description vector.
    
    Args:
    tfidf_vectors (dict): Dictionary of TF-IDF vectors for each candidate.
    jd_vector (dict): Job description vector.
    
    Returns:
    list: List of top 3 candidates with their name, score, rank, and matched skills.
    """
    # Initialize an empty list to store the ranked candidates
    ranked_candidates = []
    
    # Loop through each candidate's TF-IDF vector
    for name, tfidfvector in tfidfvectors.items():
        # Calculate the cosine similarity between the candidate's TF-IDF vector and the job description vector
        score = cosinesimilarity(tfidfvector, jd_vector)
        
        # Calculate the matched skills
        matchedskills = [skill for skill in tfidfvector if skill in jdvector and tfidfvector[skill] > 0 and jd_vector[skill] > 0]
        
        # Add the candidate to the ranked candidates list
        ranked_candidates.append({
            'name': name,
            'score': round(score, 2),
            'matchedskills': matchedskills
        })
    
    # Sort the ranked candidates list in descending order of score
    ranked_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    # Add the rank to each candidate
    for i, candidate in enumerate(ranked_candidates):
        candidate['rank'] = i + 1
    
    # Return the top 3 candidates
    return ranked_candidates[:3]