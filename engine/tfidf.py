engine/tfidf.py
import math
from engine.normalizer import normalizeskills, deduplicateskills
from engine.aliases import SKILL_ALIASES

def compute_tfidf(resumes):
    """
    Compute TF-IDF vectors for a list of resumes.
    
    Args:
    resumes (dict): Dictionary of resumes where each key is a candidate's name and each value is a string of raw skills.
    
    Returns:
    dict: Dictionary of TF-IDF vectors for each candidate.
    """
    # Initialize an empty dictionary to store the TF-IDF vectors
    tfidf_vectors = {}
    
    # Initialize an empty dictionary to store the document frequency of each skill
    df = {}
    
    # Initialize an empty set to store the vocabulary
    vocabulary = set()
    
    # Loop through each resume
    for name, raw_skills in resumes.items():
        # Normalize the skills
        normalizedskills = normalizeskills(raw_skills)
        
        # Deduplicate the skills
        deduplicatedskills = deduplicateskills(normalized_skills)
        
        # Update the vocabulary
        vocabulary.update(deduplicated_skills)
        
        # Update the document frequency of each skill
        for skill in deduplicated_skills:
            if skill not in df:
                df[skill] = 1
            else:
                df[skill] += 1
    
    # Loop through each resume again to compute the TF-IDF vectors
    for name, raw_skills in resumes.items():
        # Normalize the skills
        normalizedskills = normalizeskills(raw_skills)
        
        # Deduplicate the skills
        deduplicatedskills = deduplicateskills(normalized_skills)
        
        # Compute the TF-IDF vector
        tfidf_vector = {}
        n = len(deduplicated_skills)
        for skill in vocabulary:
            tf = 1 / n if skill in deduplicated_skills else 0
            idf = math.log(10 / df[skill]) if skill in df else 0
            tfidf = tf * idf
            tfidf_vector[skill] = tfidf
        
        # Store the TF-IDF vector
        tfidfvectors[name] = tfidfvector
    
    return tfidf_vectors

Test on the resume dataset
resumes = {
    "Arjun Sharma": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning",
    "Priya Nair": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS",
    "Rahul Gupta": "Java, Spring Boot, MySql, Microservices, Docker, kubernates",
    "Sneha Patel": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib",
    "Vikram Singh": "C++, Algoritms, Data Structure, competitive programming, python",
    "Ananya Krishnan": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD",
    "Karan Mehta": "Python, Sklearn, XGboost, feature engineering, SQL, tableau",
    "Deepika Rao": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma",
    "Aditya Kumar": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest",
    "Meera Iyer": "python, R, statistics, ML, regression, clustering, Power-BI"
}

tfidfvectors = computetfidf(resumes)

Print Sneha Patel's non-zero TF-IDF values
snehapateltfidf = tfidf_vectors["Sneha Patel"]
nonzerotfidf = {skill: tfidf for skill, tfidf in snehapateltfidf.items() if tfidf != 0}

print("Sneha Patel's non-zero TF-IDF values:")
for skill, tfidf in nonzerotfidf.items():
    print(f"{skill}: {tfidf}")