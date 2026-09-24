from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extractor import extract_skills, find_skill_gaps

job_roles = pd.read_csv(Path(__file__).parent / "data" / "job_roles.csv")

SKILL_WEIGHT = 0.7
TEXT_WEIGHT = 0.3


def match_resume(resume_text, resume_skills=None):
    """Score the resume against every role. Returns roles sorted best-first."""
    if resume_skills is None:
        resume_skills = extract_skills(resume_text)

    # Fit TF-IDF once on resume + all role descriptions so IDF weights are meaningful
    documents = [resume_text] + job_roles["description"].fillna("").tolist()
    vectors = TfidfVectorizer(stop_words="english").fit_transform(documents)
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0] * 100

    results = []
    for (_, job), similarity in zip(job_roles.iterrows(), similarities):
        required = [s.strip() for s in job["required_skills"].split(",") if s.strip()]
        matched, missing = find_skill_gaps(resume_skills, required)

        skill_score = len(matched) / len(required) * 100 if required else 0
        final = skill_score * SKILL_WEIGHT + similarity * TEXT_WEIGHT

        results.append({
            "role": job["role"],
            "score": round(final, 2),
            "skill_score": round(skill_score, 2),
            "text_similarity": round(float(similarity), 2),
            "matched_skills": matched,
            "missing_skills": missing,
        })

    return sorted(results, key=lambda r: r["score"], reverse=True)
