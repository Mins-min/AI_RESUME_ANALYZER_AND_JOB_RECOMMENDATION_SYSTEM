from text_cleaner import clean_text
from skill_extractor import (
    extract_skills,
    get_required_skills,
    find_skill_gaps
)


text = """
I am a Python developer with experience in Machine Learning,
Pandas, NumPy, SQL, FastAPI and Docker.
"""


cleaned_text = clean_text(text)

found_skills = extract_skills(cleaned_text)

print("SKILLS FOUND:")
print(found_skills)


role = "Machine Learning Engineer"

required_skills = get_required_skills(role)

matched_skills, missing_skills = find_skill_gaps(
    found_skills,
    required_skills
)


print("\nTARGET ROLE:")
print(role)

print("\nREQUIRED SKILLS:")
print(required_skills)

print("\nMATCHED SKILLS:")
print(matched_skills)

print("\nMISSING SKILLS:")
print(missing_skills)