from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from pyresparser import ResumeParser

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
        resume_data = ResumeParser(file_path).get_extracted_data()
        resume_text = pdf_reader(file_path)
        return {
            'data': resume_data,
            'text': resume_text
        }
    except Exception as e:
        raise Exception(f"Failed to parse resume: {str(e)}")