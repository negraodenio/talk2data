import sys

def extract_pdf():
    try:
        import pypdf
        with open('GenAICodingExercise.pdf', 'rb') as f:
            reader = pypdf.PdfReader(f)
            return "\n\n".join([page.extract_text() for page in reader.pages])
    except ImportError:
        pass

    try:
        import PyPDF2
        with open('GenAICodingExercise.pdf', 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n\n".join([page.extract_text() for page in reader.pages])
    except ImportError:
        pass

    try:
        import fitz # PyMuPDF
        with fitz.open('GenAICodingExercise.pdf') as doc:
            return "\n\n".join([page.get_text() for page in doc])
    except ImportError:
        pass

    return "ERROR: No suitable library found"

text = extract_pdf()
with open('pdf_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Extracted PDF to pdf_text.txt")
