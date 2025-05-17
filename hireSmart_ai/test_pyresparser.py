from pyresparser import ResumeParser
import warnings


from pyresparser import ResumeParser
data = ResumeParser('sample_resume.pdf', spacy_model='en_core_web_sm').get_extracted_data()

# Suppress any warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Parse the resume
data = ResumeParser('sample_resume.pdf').get_extracted_data()

# Print the extracted data
print(data)
