import sys
import json
import os

from PyPDF2 import PdfReader
from twth_payslip_parser.parser import parse
from twth_payslip_parser.decrypter import decrypt


def main():
    parsed = parse(
        decrypt(
            PdfReader(sys.argv[1]),
            os.getenv("PDF_PASSWORD")
        )
    )

    print(json.dumps(parsed, default=str))
