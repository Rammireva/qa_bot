import PyPDF2


# Open the PDF file in binary mode
def readFile(filename: str):
    with open(filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            print("i am her")
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Print the text from the current page
            print(text)

