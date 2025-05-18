import spacy
import sys
import os
import io
import importlib
from spacy.language import Language

# Function to check and install spaCy model
def ensure_model_installed(model_name="en_core_web_sm"):
    try:
        spacy.load(model_name)
        print(f"Model {model_name} is already installed")
    except OSError:
        print(f"Downloading {model_name}...")
        os.system(f"python -m spacy download {model_name}")

# Ensure the model is installed before anything else
ensure_model_installed()

# Monkey patch the NLP pipeline to avoid the tok2vec error
orig_pipeline_component = Language.add_pipe

def patched_add_pipe(self, factory_name, *args, **kwargs):
    # Skip problematic components
    if factory_name == "tok2vec":
        print(f"Skipping addition of tok2vec component")
        return None
    return orig_pipeline_component(self, factory_name, *args, **kwargs)

# Apply the patch
Language.add_pipe = patched_add_pipe

# Save original spacy.load
original_load = spacy.load

# Custom spacy.load function to handle model loading issues
def custom_load(name, *args, **kwargs):
    if os.path.isdir(name):
        print(f"Loading default model instead of directory: {name}")
        return original_load("en_core_web_sm", *args, **kwargs)
    return original_load(name, *args, **kwargs)

# Apply patches globally
spacy.load = custom_load
sys.modules["spacy"].load = custom_load

# PDF text extraction using pdfminer3
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter

def pdf_reader(file_path):
    """Extract text from PDF file"""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text

def clean_data(data_dict):
    """Clean and normalize data from the resume parser"""
    cleaned = {}
    for key, value in data_dict.items():
        if isinstance(value, list):
            cleaned[key] = [str(v).strip().lower() for v in value if v is not None]
        elif isinstance(value, (int, float)):
            cleaned[key] = str(value).strip().lower()
        elif isinstance(value, str):
            cleaned[key] = value.strip().lower()
        elif value is None:
            cleaned[key] = ""
        else:
            cleaned[key] = str(value).strip().lower()
    return cleaned

def parse_resume(file_path):
    """Parse resume using pyresparser with error handling"""
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        # Only import pyresparser after applying all patches
        from pyresparser import ResumeParser
        
        raw_data = ResumeParser(file_path).get_extracted_data()
        resume_data = clean_data(raw_data)
        resume_text = pdf_reader(file_path)
        
        return {
            'data': resume_data,
            'text': resume_text
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details:\n{error_details}")
        raise Exception(f"Failed to parse resume: {str(e)}")

if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Replace with your actual path
    result = parse_resume(file_path)
    print(result)