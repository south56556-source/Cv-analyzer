# CV Analyzer

A simple Python project for comparing a CV against a job description and calculating how well the CV matches the required skills and keywords.

## Project structure

- `src/main.py` - main application logic
- `data/cvs/` - folder for CV files
- `data/job_descriptions/` - folder for job description files
- `tests/` - placeholder for automated tests

## Quick start

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analyzer:
   ```bash
   python src/main.py data/cvs/sample_cv.txt data/job_descriptions/sample_job_description.txt
   ```

## How it works

The script reads the CV and job description text, extracts candidate keywords, and calculates a match percentage based on overlap between them.

This is intentionally lightweight and easy to extend for more advanced CV screening features later.
