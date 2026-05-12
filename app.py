from pathlib import Path

from data.job_description import JOB_DESCRIPTIONS
from data.resumes import RESUMES
from engine.matcher import rank_candidates
from engine.normalizer import deduplicate_skills, normalize_skills
from engine.tfidf import compute_tfidf


def build_vocabulary(resumes):
    vocabulary = set()
    for raw_skills in resumes.values():
        vocabulary.update(deduplicate_skills(normalize_skills(raw_skills)))
    return sorted(vocabulary)


def build_job_vector(raw_skills, vocabulary):
    skills = set(deduplicate_skills(normalize_skills(raw_skills)))
    return {skill: 1 if skill in skills else 0 for skill in vocabulary}


def format_results(jd_id, jd_data, ranked_candidates):
    header = f"{jd_id} Result: Top 5 Candidates with Matching Scores."
    body = ", ".join(f"{candidate['name']}({candidate['score']:.2f})" for candidate in ranked_candidates)
    return f"{header}\ne.g. {body}\n*"


def main():
    vocabulary = build_vocabulary(RESUMES)
    tfidf_vectors = compute_tfidf(RESUMES)

    output_lines = []
    for jd_id, jd_data in JOB_DESCRIPTIONS.items():
        jd_vector = build_job_vector(jd_data["skills"], vocabulary)
        ranked_candidates = rank_candidates(tfidf_vectors, jd_vector)
        output_lines.append(format_results(jd_id, jd_data, ranked_candidates))

    output_text = "\n\n".join(output_lines)
    print(output_text)

    output_path = Path(__file__).resolve().parent / "output" / "results.txt"
    output_path.write_text(output_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()