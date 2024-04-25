import pdfquery
import tempfile
from PyPDF2 import PdfWriter

def decrypt(file, password):
    if file.is_encrypted:
        file.decrypt(password)

        with tempfile.NamedTemporaryFile() as tf:
            out = PdfWriter()

            for idx in range(len(file.pages)):
                page = file.pages[idx]
                out.add_page(page)

            out.write(tf)

            pdf = pdfquery.PDFQuery(tf)
            pdf.load()

            return pdf
    else:
        return file
