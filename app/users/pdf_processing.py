import fitz
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import PDFPageAggregator


def is_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(4)
            return header == b'%PDF'
    except Exception as e:
        print(f"Error: {e}")
        return False


def extract_information_between_keywords(pdf_path,start_keyword,end_keyword):
    extracted_information = []
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return f"Error opening PDF: {e}"

    for page_num in range(doc.page_count):
        page = doc[page_num]
        try:
            page_text = page.get_text()
        except Exception as e:
            return f"Error extracting text from PDF: {e}"

        pattern = re.compile(f'{start_keyword}(.*?){end_keyword}', re.DOTALL | re.IGNORECASE)
        try:
            matches = pattern.findall(page_text)
        except Exception as e:
            return f"Error with regex pattern: {e}"

        for match in matches:
            try:
                location = match.rsplit(',', 1)[-1].strip()
            except Exception as e:
                return f"Error splitting match: {e}"
            extracted_information.append(location)
    try:
        doc.close()
    except Exception as e:
        return f"Error closing PDF: {e}"

    return extracted_information

def save_file(file, path):
    try:
        file.save(path)
    except Exception as e:
        return f"Error saving file: {e}"

def extract_info_from_pdf(path):
    with open(path, 'rb') as file:
        extracted_info = extract_information_between_keywords(file ,"Domicilio:","Sucursales:")
        extracted_ruts = extract_information_between_keywords(file,"RUT del emisor:" , "Fecha de generación de la carpeta:")
        extracted_rut = extracted_ruts[0] if extracted_ruts else None
    return extracted_info, extracted_rut

def check_comunas(extracted_info, comunas):
    comunas_lower = [comuna.lower() for comuna in comunas]
    for info in extracted_info:
        if info.lower() in comunas_lower:
            return True
    return False



