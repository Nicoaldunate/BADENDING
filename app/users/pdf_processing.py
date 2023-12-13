import fitz
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import PDFPageAggregator

def open_pdf(file):
    parser = PDFParser(file)
    document = PDFDocument(parser)
    return document

def get_layout(document):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        yield layout

def extract_text(layout, positions):
    result_text = ""
    for element in layout:
        if isinstance(element, LTTextBox):
            x, y, text = element.bbox[0], element.bbox[3], element.get_text()
            for position in positions:
                x1, y1, x2, y2 = position
                if x1 < x < x2 and y1 < y < y2:
                    result_text = text
                    return result_text
    return result_text

def extract_text_by_position(pdf_path):
    positions = [(415, 347, 416, 350)]  
    document = open_pdf(pdf_path)
    for layout in get_layout(document):
        result_text = extract_text(layout, positions)
        if result_text:
            break
    return result_text



def extract_information_between_keywords(pdf_path):
    extracted_information = []
    start_keyword = "Domicilio:"
    end_keyword = "Sucursales:"

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
        extracted_info = extract_information_between_keywords(file)
        extracted_rut = extract_text_by_position(file).strip()
    return extracted_info, extracted_rut    

def check_comunas(extracted_info, comunas):
    comunas_lower = [comuna.lower() for comuna in comunas]
    for info in extracted_info:
        if info.lower() in comunas_lower:
            return True
    return False



