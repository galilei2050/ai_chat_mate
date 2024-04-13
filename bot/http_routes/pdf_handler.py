import PyPDF2

def extract_text_from_pdf(pdf_path):
    pages = []
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # Iterate through each page
        for page in reader.pages:
            pages.append(page.extract_text())
        return pages

if __name__ == "__main__":
    pdf_path = 'misc/samples/pitchdeck.pdf'
    pdf_text = extract_text_from_pdf(pdf_path)
    for page in pdf_text:
        print(page)
