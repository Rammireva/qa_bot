import PyPDF2
from typing import List, Dict
import re

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

def verify_pdf_path(file_path):
    try:
        print(file_path)
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            if len(pdf_reader.pages) > 0:
                pass
            else:
                raise("PDF file is empty")
    except PyPDF2.errors.PdfReadError:
        raise PyPDF2.errors.PdfReadError("Invalid PDF file")
    except FileNotFoundError:
        raise FileNotFoundError("File not found, check file address again")
    except Exception as e:
        raise(f"Error: {e}")

def get_text_chunks(text: str, word_limit: int) -> List[str]:
    """
    Divide a text into chunks with a specified word limit while ensuring each chunk contains complete sentences.

    Parameters:
        text (str): The entire text to be divided into chunks.
        word_limit (int): The desired word limit for each chunk.

    Returns:
        List[str]: A list containing the chunks of texts with the specified word limit and complete sentences.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        words = sentence.split()
        if len(" ".join(current_chunk + words)) <= word_limit:
            current_chunk.extend(words)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = words

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def load_pdf(file: str, word: int) -> Dict[int, List[str]]:
    reader = PyPDF2.PdfReader(file)
    documents = {}
    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        texts = page.extract_text()
        text_chunks = get_text_chunks(texts, word)
        documents[page_no] = text_chunks
    return documents




