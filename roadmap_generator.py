"""Learning roadmap: RAG/LLM when available, rule-based fallback otherwise."""

# Practical, beginner-friendly one-liners for common skills
SKILL_TIPS = {
    "python": "Learn syntax, functions, OOP and virtual environments.",
    "sql": "Practise SELECT, JOIN, GROUP BY and window functions.",
    "excel": "Learn formulas, pivot tables and charts.",
    "pandas": "Practise cleaning, filtering and aggregating DataFrames.",
    "numpy": "Learn arrays, broadcasting and vectorised operations.",
    "power bi": "Build a dashboard from a real dataset.",
    "tableau": "Build interactive charts and dashboards.",
    "statistics": "Cover distributions, hypothesis testing and correlation.",
    "data visualization": "Practise Matplotlib/Plotly and choosing the right chart.",
    "machine learning": "Learn supervised learning, train/test split and evaluation metrics.",
    "scikit-learn": "Train, tune and evaluate models with pipelines.",
    "deep learning": "Understand neural networks, backpropagation and training loops.",
    "tensorflow": "Build and train a small model with Keras.",
    "pytorch": "Learn tensors, autograd and writing a training loop.",
    "fastapi": "Build a REST API that serves a model prediction.",
    "docker": "Containerise a Python app and run it locally.",
    "git": "Learn commits, branches and pull requests on GitHub.",
    "apis": "Learn REST basics and call/build simple APIs.",
    "llm": "Learn prompting and calling a hosted LLM API.",
    "rag": "Build a small retrieval + generation pipeline.",
    "langchain": "Build a chain with a retriever and an LLM.",
    "nlp": "Cover tokenisation, embeddings and text classification.",
    "transformers": "Understand attention and use pretrained models.",
    "hugging face": "Load and fine-tune a pretrained model with the Transformers library.",
    "opencv": "Practise image loading, filtering and contour detection.",
    "cnn": "Train a small CNN on an image dataset.",
    "yolo": "Run and fine-tune YOLO for object detection.",
}


def rule_based_roadmap(missing_skills):
    lines = []
    for i, skill in enumerate(missing_skills, start=1):
        tip = SKILL_TIPS.get(skill.lower(), "Start with an introductory tutorial, then build a mini project.")
        lines.append(f"**Week {i}: {skill}**  \n{tip}")
    return "\n\n".join(lines)


def generate_roadmap(missing_skills, role=None):
    """Returns (roadmap_markdown, source) where source is 'AI (RAG)' or 'Rule-based'."""
    if not missing_skills:
        return "You already have all the required skills for this role.", "None needed"

    try:
        from rag_pipeline import api_key_available, get_rag_response

        if api_key_available():
            skills = ", ".join(missing_skills)
            question = (
                f"Create a simple, practical, beginner-friendly learning roadmap"
                f"{' for a ' + role if role else ''} covering these missing skills: {skills}. "
                "Arrange them in logical learning order and briefly explain what to learn for each."
            )
            text = get_rag_response("", question, retrieval_query=f"{role or ''} {skills}")
            if text.strip():
                return text, "AI (RAG)"
    except Exception:
        pass  # fall back to rules below

    return rule_based_roadmap(missing_skills), "Rule-based"
