# AI Resume Analyzer and Job Recommendation System

An intelligent, full-stack career development platform powered by Python, Streamlit, LangChain, FAISS, and Google Gemini AI. This application parses resumes, extracts technical and soft skills, matches candidates with ideal job roles using semantic search and machine learning, generates personalized skill-gap roadmaps, and features an interactive RAG chatbot for career mentoring.

---

## 🚀 Key Features

1. **Smart Resume Parsing**: Extracts text seamlessly from PDF and DOCX resume formats.
2. **Skill Extraction & Analysis**: Identifies core technical skills, programming languages, tools, and methodologies.
3. **Job Recommendation & Scoring**: Evaluates candidate fit against job role datasets using TF-IDF / Cosine Similarity and machine learning metrics.
4. **Personalized Upskilling Roadmap**: Identifies skill gaps and provides targeted recommendations to bridge them.
5. **Interactive RAG Chatbot**: Powered by LangChain, FAISS, and Google Gemini to answer career and resume-related queries.
6. **Professional Report Generation**: Generates downloadable PDF/Word analysis reports using ReportLab.

---

## 🛠️ Tech Stack

* **Frontend & Backend**: Streamlit (Python)
* **AI & LLM Integration**: Google Gemini API (`langchain-google-genai`), LangChain
* **Vector Database**: FAISS (Facebook AI Similarity Search)
* **Machine Learning & NLP**: Scikit-learn, Pandas, NumPy
* **Document Processing & Export**: PyPDF, python-docx, ReportLab

---

## 📂 Project Structure

```text
AI_RESUME_ANALYZER_AND_JOB_RECOMMENDATION_SYSTEM/
│
├── app.py                 # Main Streamlit application entry point
├── job_matcher.py         # Job role matching and scoring logic
├── rag_pipeline.py        # LangChain & FAISS RAG chatbot module
├── roadmap_generator.py   # AI-driven career path and skill-gap generator
├── skill_extractor.py     # NLP-based skill extraction utilities
├── text_cleaner.py        # Text preprocessing and normalization helpers
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation