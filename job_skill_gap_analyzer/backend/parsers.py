import pdfplumber
from io import BytesIO

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if t.strip():
                text_parts.append(t)
    return "\n".join(text_parts).strip()
