import PyPDF2

def load_pdf(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text[:8000]
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
