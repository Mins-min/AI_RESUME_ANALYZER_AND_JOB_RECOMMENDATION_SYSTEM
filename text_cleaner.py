import re


def clean_text(text):
    """Clean resume text while keeping technical tokens (C++, C#, .NET, scikit-learn)."""
    text = re.sub(r"\bc\s*\+\s*\+", "C++", text, flags=re.I)
    text = re.sub(r"\bc\s*#", "C#", text, flags=re.I)
    text = re.sub(r"\.\s*net\b", ".NET", text, flags=re.I)

    paragraphs = []
    for paragraph in text.split("\n\n"):
        # Keep hyphens and slashes so "scikit-learn" and "CI/CD" survive
        paragraph = re.sub(r"[^\w\s+#./\-\n]", " ", paragraph)
        paragraph = re.sub(r"[ \t]+", " ", paragraph).strip()
        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)
