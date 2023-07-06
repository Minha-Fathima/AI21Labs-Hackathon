import PyPDF2


def pdfToText(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        text += page.extract_text()
    return text
