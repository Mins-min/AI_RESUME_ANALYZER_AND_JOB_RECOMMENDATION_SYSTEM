from pypdf import PdfReader
from docx import Document


def extract_text(file):

    # Get file name
    if hasattr(file, "filename"):
        file_name = file.filename
        file_object = file.file
    else:
        file_name = file.name
        file_object = file

    # PDF
    if file_name.endswith(".pdf"):

        reader = PdfReader(file_object)

        paragraphs = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                paragraphs.append(page_text)

        return "\n\n".join(paragraphs)

    # DOCX
    elif file_name.endswith(".docx"):

        document = Document(file_object)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n\n".join(paragraphs)

    else:

        return "Unsupported file type"