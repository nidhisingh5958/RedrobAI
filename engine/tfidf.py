import math

from engine.normalizer import deduplicate_skills, normalize_skills


def _prepare_resume_skills(resumes):
    prepared_skills = {}
    vocabulary = set()

    for candidate_name, raw_skills in resumes.items():
        skills = deduplicate_skills(normalize_skills(raw_skills))
        prepared_skills[candidate_name] = skills
        vocabulary.update(skills)

    return prepared_skills, sorted(vocabulary)


def compute_tfidf(resumes):
    """Compute TF-IDF vectors for each candidate resume."""
    prepared_skills, vocabulary = _prepare_resume_skills(resumes)
    document_frequency = {skill: 0 for skill in vocabulary}

    for skills in prepared_skills.values():
        for skill in skills:
            document_frequency[skill] += 1

    total_documents = len(prepared_skills)
    tfidf_vectors = {}

    for candidate_name, skills in prepared_skills.items():
        unique_skill_count = len(skills)
        tfidf_vector = {}

        for skill in vocabulary:
            if skill not in skills or unique_skill_count == 0:
                tfidf_vector[skill] = 0.0
                continue

            term_frequency = 1 / unique_skill_count
            inverse_document_frequency = math.log(total_documents / document_frequency[skill])
            tfidf_vector[skill] = term_frequency * inverse_document_frequency

        tfidf_vectors[candidate_name] = tfidf_vector

    return tfidf_vectors


def build_vocabulary(resumes):
    """Build the shared vocabulary from normalized and deduplicated resume skills."""
    _, vocabulary = _prepare_resume_skills(resumes)
    return vocabulary