import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Set LLM_MODEL in .env to change the model without touching code
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = "models/gemini-embedding-001"


def api_key_available():
    return bool(os.getenv("GOOGLE_API_KEY"))


@lru_cache(maxsize=1)
def create_vector_database():
    """Built once per process, not once per question."""
    documents = DirectoryLoader(
        "knowledge_base", glob="**/*.txt", loader_cls=TextLoader
    ).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    ).split_documents(documents)
    return FAISS.from_documents(
        chunks, GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    )


def get_rag_response(resume_text, question, retrieval_query=None):
    retriever = create_vector_database().as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(retrieval_query or question)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
You are an AI Resume Analyzer giving career guidance to students.

Retrieved Knowledge:
{context}

Resume (may be empty):
{resume_text}

Task:
{question}

Rules:
- Base advice on the retrieved knowledge; do not invent tools or courses.
- Do not make hiring decisions.
- Do not use gender, age, religion, nationality, photograph,
  marital status or disability.
- Remind the reader that a missing keyword does not mean missing ability.

Answer:
"""
    response = ChatGoogleGenerativeAI(model=LLM_MODEL).invoke(prompt)
    content = response.content

    # Some models return a list of content blocks
    if isinstance(content, list):
        content = "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        )
    return content
