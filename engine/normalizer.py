engine/normalizer.py
from engine.aliases import SKILL_ALIASES

def normalizeskills(rawskills):
    """
    Normalize raw skills by handling multi-word phrases first, then single tokens.
    
    Args:
    raw_skills (str): Raw skills string.
    
    Returns:
    list: List of normalized skills.
    """
    # Split raw skills into individual tokens
    tokens = raw_skills.lower().replace(',', ' ').split()
    
    # Initialize an empty list to store normalized skills
    normalized_skills = []
    
    # Initialize an index to track the current position in the tokens list
    i = 0
    
    # Loop through the tokens list
    while i < len(tokens):
        # Check for multi-word phrases first
        for phrase in [key for key in SKILL_ALIASES if ' ' in key]:
            if ' '.join(tokens[i:i + len(phrase.split())]) == phrase:
                # If a multi-word phrase is found, add its alias to the normalized skills list
                normalizedskills.append(SKILLALIASES[phrase])
                # Move the index forward by the length of the phrase
                i += len(phrase.split())
                break
        else:
            # If no multi-word phrase is found, check for single tokens
            if tokens[i] in SKILL_ALIASES:
                # If a single token is found, add its alias to the normalized skills list
                normalizedskills.append(SKILLALIASES[tokens[i]])
            # Move the index forward by 1
            i += 1
    
    return normalized_skills

def deduplicate_skills(skills):
    """
    Deduplicate skills by removing duplicates and keeping only unique skills.
    
    Args:
    skills (list): List of skills.
    
    Returns:
    list: List of deduplicated skills.
    """
    # Use a set to remove duplicates and convert back to a list
    return list(set(skills))

Test on Rahul Gupta's raw skills
raw_skills = "Java, Spring Boot, MySql, Microservices, Docker, kubernates"
normalizedskills = normalizeskills(raw_skills)
deduplicatedskills = deduplicateskills(normalized_skills)

print("Raw Skills:", raw_skills)
print("Normalized Skills:", normalized_skills)
print("Deduplicated Skills:", deduplicated_skills)