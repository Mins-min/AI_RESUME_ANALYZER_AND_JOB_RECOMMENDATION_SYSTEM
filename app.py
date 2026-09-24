import io
import os
import streamlit as st
import pandas as pd
import numpy as np
from pypdf import PdfReader
from docx import Document

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Streamlit Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Job Recommendation System",
    page_icon="📄",
    layout="wide"
)

# --- Helper Functions for File Processing ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# --- Mock Analysis Engine (Replace with your actual NLP/Matching logic) ---
PREDEFINED_ROLES = {
    "AI/ML Intern": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy", "Scikit-learn", "Git", "Statistics"],
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy", "Scikit-learn", "Statistics", "Matplotlib", "Power BI"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "LLM", "RAG", "LangChain", "APIs", "FastAPI", "Git"]
}

def analyze_resume(resume_text):
    text_lower = resume_text.lower()
    
    # Simple keyword extraction check based on common skills
    all_possible_skills = ["python", "java", "c", "sql", "mysql", "machine learning", "pandas", "numpy", "scikit-learn", "git", "statistics", "deep learning", "llm", "rag", "langchain", "apis", "fastapi"]
    found_skills = [skill.title() for skill in all_possible_skills if skill in text_lower]
    
    role_matches = {}
    for role, required_skills in PREDEFINED_ROLES.items():
        matched = [s for s in required_skills if s in found_skills]
        missing = [s for s in required_skills if s not in found_skills]
        score = (len(matched) / len(required_skills)) * 100 if required_skills else 0
        role_matches[role] = {
            "score": round(score, 2),
            "matched": matched,
            "missing": missing
        }
        
    return found_skills, role_matches

# --- PDF Report Generation Function ---
def generate_pdf_report(resume_name, found_skills, role_matches, target_role):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#444444'),
        spaceAfter=4
    )
    
    story = []
    
    # Title & Header
    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(Paragraph(f"<b>Analyzed Resume:</b> {resume_name}", body_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc'), spaceAfter=15))
    
    # Found Skills
    story.append(Paragraph("Extracted Skills", heading_style))
    skills_str = ", ".join(found_skills) if found_skills else "None detected"
    story.append(Paragraph(skills_str, body_style))
    story.append(Spacer(1, 10))
    
    # Role Recommendations
    story.append(Paragraph("Top Role Recommendations & Skill Gaps", heading_style))
    for role, data in role_matches.items():
        story.append(Paragraph(f"<b>{role}</b> - Match Score: {data['score']}%", body_style))
        story.append(Paragraph(f"&nbsp;&nbsp;• <b>Matched Skills:</b> {', '.join(data['matched']) if data['matched'] else 'None'}", body_style))
        story.append(Paragraph(f"&nbsp;&nbsp;• <b>Missing Skills:</b> {', '.join(data['missing']) if data['missing'] else 'None'}", body_style))
        story.append(Spacer(1, 6))
        
    story.append(Spacer(1, 10))
    
    # Target Role Roadmap section
    if target_role in role_matches:
        story.append(Paragraph(f"Learning Roadmap for: {target_role}", heading_style))
        missing_list = role_matches[target_role]["missing"]
        if missing_list:
            for idx, skill in enumerate(missing_list, 1):
                story.append(Paragraph(f"&nbsp;&nbsp;Week {idx}: Focus on <b>{skill}</b> - Practice core concepts, hands-on projects, and documentation.", body_style))
        else:
            story.append(Paragraph("No critical missing skills found for this role! You are fully prepared.", body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# --- Streamlit UI Layout ---
st.title("AI Resume Analyzer and Job Recommendation System")
st.write("Upload your resume to analyze your skills and find suitable job roles.")

uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileSize": f"{uploaded_file.size / 1024:.1f}KB"}
    st.success(f"Resume uploaded: {file_details['FileName']} ({file_details['FileSize']})")
    
    # Extract text based on file format
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = ""

    with st.expander("View extracted resume text"):
        st.text(resume_text)
        
    # Perform Analysis
    found_skills, role_matches = analyze_resume(resume_text)
    
    st.subheader("Skills Found")
    if found_skills:
        # Render skills as bullet points instead of Python list syntax
        for skill in found_skills:
            st.markdown(f"- {skill}")
    else:
        st.write("No explicit skills recognized automatically.")
        
    st.subheader("Top Role Recommendations")
    
    # Sort roles by match score descending
    sorted_roles = sorted(role_matches.items(), key=lambda x: x[1]["score"], reverse=True)
    
    for rank, (role, data) in enumerate(sorted_roles, 1):
        st.markdown(f"### {rank}. {role}")
        st.write(f"**Match Score:** {data['score']}%")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Matched Skills:**")
            if data["matched"]:
                for s in data["matched"]:
                    st.markdown(f"- {s}")
            else:
                st.markdown("- None")
                
        with col2:
            st.markdown("**Missing Skills:**")
            if data["missing"]:
                for s in data["missing"]:
                    st.markdown(f"- {s}")
            else:
                st.markdown("- None")
        st.divider()

    # Skill Gap and Learning Roadmap
    st.subheader("Skill Gap and Learning Roadmap")
    target_role = st.selectbox("Choose your target role", list(PREDEFINED_ROLES.keys()))
    
    if target_role in role_matches:
        st.markdown(f"### Roadmap for becoming a {target_role}")
        missing_skills = role_matches[target_role]["missing"]
        
        st.markdown("**Missing skills:**")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- {skill}")
                
            st.markdown("### Suggested Weekly Plan:")
            for idx, skill in enumerate(missing_skills, 1):
                st.markdown(f"- **Week {idx}: {skill}** — Practice foundational concepts, hands-on tutorials, and project implementation.")
        else:
            st.success("You possess all necessary core skills for this target role!")

    st.markdown("---")
    
    # PDF Download Button
    pdf_report_bytes = generate_pdf_report(uploaded_file.name, found_skills, role_matches, target_role)
    
    st.download_button(
        label="📥 Download Full Report as PDF",
        data=pdf_report_bytes,
        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_Analysis_Report.pdf",
        mime="application/pdf"
    )