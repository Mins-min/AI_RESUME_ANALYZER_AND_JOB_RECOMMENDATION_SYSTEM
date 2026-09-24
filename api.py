from fastapi import FastAPI, UploadFile, File
from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import match_resume

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running"}


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    resume_text = extract_text(file)

    cleaned_text = clean_text(resume_text)

    skills = extract_skills(cleaned_text)

    results = match_resume(cleaned_text)

    return {
        "skills": skills,
        "top_roles": results[:3]
    }