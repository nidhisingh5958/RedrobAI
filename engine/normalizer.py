from engine.aliases import SKILL_ALIASES


def normalize_skills(raw_skills):
    """Normalize a comma-separated raw skill string into canonical skills."""
    normalized_skills = []

    for chunk in raw_skills.split(','):
        token = chunk.strip().lower()
        if not token:
            continue

        canonical_skill = SKILL_ALIASES.get(token)
        if canonical_skill:
            normalized_skills.append(canonical_skill)

    return normalized_skills


def deduplicate_skills(skills):
    """Remove duplicates while preserving the first occurrence order."""
    deduplicated_skills = []
    seen = set()

    for skill in skills:
        if skill in seen:
            continue
        seen.add(skill)
        deduplicated_skills.append(skill)

    return deduplicated_skills