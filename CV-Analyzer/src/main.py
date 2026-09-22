import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader


load_dotenv()


def normalize_keyword(value):
    """Convert a text token to a comparable lowercase identifier."""
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


def compute_match_score(cv_text, job_description):
    """Return a 0-100 match score based on keyword overlap between a CV and a job description."""
    if not cv_text or not job_description:
        return 0.0

    cv_tokens = {
        normalize_keyword(token)
        for token in re.findall(r"[A-Za-z0-9+#.\-/]+", cv_text.lower())
        if normalize_keyword(token)
    }
    job_tokens = {
        normalize_keyword(token)
        for token in re.findall(r"[A-Za-z0-9+#.\-/]+", job_description.lower())
        if normalize_keyword(token)
    }

    if not job_tokens:
        return 0.0

    overlap = cv_tokens & job_tokens
    score = (len(overlap) / len(job_tokens)) * 100.0
    return round(100.0 if score >= 100.0 else score, 2)


def extract_text_from_pdf(pdf_file):
    """Extract text content from an uploaded PDF file."""
    if pdf_file is None:
        return ""

    file_obj = pdf_file
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)

    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def get_groq_client():
    """Create a Groq client if an API key is available."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def analyze_cv(cv_text, job_description=""):
    """Send CV text to Groq API for skill extraction, scoring, and improvement suggestions."""
    if not cv_text or not cv_text.strip():
        raise ValueError("CV text is empty.")

    client = get_groq_client()
    if client is None:
        raise RuntimeError("Missing GROQ_API_KEY. Add it to your .env file before running AI analysis.")

    prompt = f"""
    You are an expert HR recruiter and resume reviewer. Analyze the following CV text.

    CV Text:
    {cv_text}

    Job Description (Optional Context):
    {job_description if job_description else "General Software/Tech Role"}

    Please provide your response strictly formatted as follows:

    ### 1. Extracted Skills
    List key technical and soft skills identified.

    ### 2. Match Score
    Provide an overall score out of 100 with a 1-2 sentence justification.

    ### 3. Suggested Improvements
    Provide 3 to 5 actionable tips to improve the CV.
    """

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def run_cli(cv_path, job_path):
    """Simple CLI entrypoint used by the README example."""
    cv_text = Path(cv_path).read_text(encoding="utf-8", errors="ignore")
    job_text = Path(job_path).read_text(encoding="utf-8", errors="ignore")
    score = compute_match_score(cv_text, job_text)
    print(f"Match Score: {score:.2f}/100")


def render_streamlit_app():
    """Build the Streamlit interface."""
    st.set_page_config(page_title="CV Analyzer", page_icon="📄")
    st.title("📄 AI CV Analyzer")
    st.write("Upload your resume/CV (PDF) to extract skills, get a score, and receive feedback.")

    uploaded_file = st.file_uploader("Upload CV (PDF format)", type=["pdf"])
    job_desc = st.text_area("Job Description (Optional)", placeholder="Paste target job description here...")

    if st.button("Analyze CV"):
        if uploaded_file is not None:
            with st.spinner("Extracting text and analyzing with AI..."):
                try:
                    cv_text = extract_text_from_pdf(uploaded_file)
                    if cv_text.strip():
                        analysis_result = analyze_cv(cv_text, job_desc)
                        st.success("Analysis Complete!")
                        st.markdown(analysis_result)
                    else:
                        st.error("Could not extract text from the PDF. Please ensure it is not a scanned image.")
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")
        else:
            st.warning("Please upload a PDF file first.")


if __name__ == "__main__":
    render_streamlit_app()
