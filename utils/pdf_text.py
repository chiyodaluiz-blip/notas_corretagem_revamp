import pdfplumber


def extract_text(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            t = page.extract_text()

            if t:
                text += "\n" + t

    return text