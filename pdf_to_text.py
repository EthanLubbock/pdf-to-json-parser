import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

### Helper functions for data cleaning ###

PRICE_WORDS = ["ten", "twelve", "fifteen", "twenty"] #TODO: expand to more cases
def fix_price_words(text):
    price_words_pattern = "|".join(PRICE_WORDS)
    # Define regex to match S followed by either numbers or price-like words
    price_pattern = re.compile(r"\bS(\d+|(?:{}))\b".format(price_words_pattern), re.IGNORECASE)

    # Replace 'S' with '$' in the matched patterns
    corrected_text = price_pattern.sub(r"$\1", text)
    return corrected_text

def clean_ocr_text(text):
    # Run price words to catch $ processed as S
    text = fix_price_words(text)
    #TODO: include other data cleaning as appropriate
    return text

### Functions for text extraction ###

def extract_text_from_image_pdf(pdf_path, dpi=300):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=dpi)
    extracted_text = []
    
    for page_number, image in enumerate(images, start=1):
        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        if text.strip():  # Only keep non-empty results
            text = clean_ocr_text(text)
            extracted_text.append((page_number, text.strip()))
    
    return extracted_text

def extract_text_hybrid(pdf_path):
    extracted_text = []

    # Attempt text extraction using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text.strip():
                extracted_text.append((page_number, text.strip()))
        pdf.close()

    # If no text found, fallback to OCR
    if not extracted_text:
        extracted_text = extract_text_from_image_pdf(pdf_path)
    
    extracted_text = "\n".join([
        f"Page {page_num}: {chunk}" for page_num, chunk in extracted_text
    ])
    return extracted_text

if __name__ == "__main__":
    # Test function
    pdf_path = "./example_pdfs/bacardi_menu.pdf"
    hybrid_text = extract_text_hybrid(pdf_path)
    print(hybrid_text)