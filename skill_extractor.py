import re
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

skills = pd.read_csv(DATA_DIR / "skill_dictionary.csv")
job_roles = pd.read_csv(DATA_DIR / "job_roles.csv")

# Compile once. Lookarounds instead of \b so C++, C# and .NET match correctly.
_PATTERNS = {
    skill: re.compile(r"(?<![\w+#])" + re.escape(skill.lower()) + r"(?![\w+#])")
    for skill in skills["skill"]
}


def extract_skills(text):
    lowered = text.lower()
    return [skill for skill, pattern in _PATTERNS.items() if pattern.search(lowered)]


def group_skills_by_category(found_skills):
    """Group skills by the optional 'category' column of skill_dictionary.csv."""
    if "category" not in skills.columns:
        return {"Skills": list(found_skills)}
    lookup = dict(zip(skills["skill"], skills["category"]))
    grouped = {}
    for skill in found_skills:
        grouped.setdefault(lookup.get(skill, "Other"), []).append(skill)
    return grouped


def get_required_skills(role):
    job = job_roles[job_roles["role"] == role]
    if job.empty:
        return []
    return [s.strip() for s in job.iloc[0]["required_skills"].split(",")]


def find_skill_gaps(found_skills, required_skills):
    found = {s.lower() for s in found_skills}
    matched = [s for s in required_skills if s.lower() in found]
    missing = [s for s in required_skills if s.lower() not in found]
    return matched, missing
