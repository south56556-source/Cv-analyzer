from __future__ import annotations

import argparse
import re
from pathlib import Path


def normalize_words(text: str) -> set[str]:
    """Return a set of normalized keywords from the input text."""
    return {
        word.lower()
        for word in re.findall(r"[A-Za-z][A-Za-z0-9+\-\.]*", text)
        if len(word) > 2
    }


def compute_match_score(cv_text: str, job_description: str) -> float:
    """Calculate a simple keyword match percentage between a CV and job description."""
    cv_keywords = normalize_words(cv_text)
    job_keywords = normalize_words(job_description)

    if not job_keywords:
        return 0.0

    overlap = cv_keywords & job_keywords
    score = (len(overlap) / len(job_keywords)) * 100
    return round(score, 2)


def read_text_file(path: str | Path) -> str:
    """Read the content of a text file."""
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare a CV against a job description.")
    parser.add_argument("cv_path", help="Path to the CV text file")
    parser.add_argument("job_description_path", help="Path to the job description text file")
    args = parser.parse_args()

    cv_text = read_text_file(args.cv_path)
    job_description = read_text_file(args.job_description_path)

    score = compute_match_score(cv_text, job_description)

    print(f"CV match score: {score}%")


if __name__ == "__main__":
    main()
