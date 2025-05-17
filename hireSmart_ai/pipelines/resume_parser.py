import spacy
import pyresparser.resume_parser

# Monkey patch pyresparser's spacy.load to load "en_core_web_sm" instead of its own folder
def fixed_spacy_load(name, *args, **kwargs):
    import os
    rp_dir = os.path.dirname(os.path.abspath(pyresparser.resume_parser.__file__))
    if name == rp_dir:
        return spacy.load("en_core_web_sm")
    else:
        return spacy.load(name, *args, **kwargs)

pyresparser.resume_parser.spacy.load = fixed_spacy_load

from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io


def pdf_reader(file_path):
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


def parse_resume(file_path):
    try:
        # Use ResumeParser normally - now patched to load proper spacy model
        resume_data = ResumeParser(file_path).get_extracted_data()
        resume_text = pdf_reader(file_path)
        return {
            'data': resume_data,
            'text': resume_text
        }
    except Exception as e:
        raise Exception(f"Failed to parse resume: {str(e)}")


if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Change to your PDF resume path
    result = parse_resume(file_path)
    print(result)
