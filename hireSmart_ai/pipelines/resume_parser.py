import spacy
import re
from pdfminer.high_level import extract_text

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Extract text from PDF file
def extract_pdf_text(file_path):
    return extract_text(file_path)

# Extract email using regex
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

# Extract phone number
def extract_phone(text):
    match = re.search(r'(\+?\d{1,3})?[-.\s]?\(?\d{3,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else None

# Extract name using spaCy (first PERSON entity)
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

# Basic keyword-based skills extraction
def extract_skills(text, skill_set):
    found = []
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return found

# Main resume parser
def parse_resume(file_path):
    text = extract_pdf_text(file_path)
    skills_list = ['Python', 'Java', 'C++', 'SQL', 'Machine Learning', 'Data Analysis', 'Excel', 'AWS']

    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text, skills_list),
        'preview_text': text[:300] + "..."  # Optional
    }

# Run the parser
if __name__ == "__main__":
    path = "sample_resume.pdf"  # ← change to your file path
    try:
        result = parse_resume(path)
        print(result)
    except Exception as e:
        print("Error processing resume:", str(e))

