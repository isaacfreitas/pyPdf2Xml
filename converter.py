import fitz  # PyMuPDF
import xml.etree.ElementTree as ET

def pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text
#==========================================================================
def text_to_xml(text):
    root = ET.Element("Document")
    # Exemplo: Criando uma tag com o texto extraído
    content = ET.SubElement(root, "Content")
    content.text = text

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)
#==========================================================================
if __name__ == "__main__":
    pdf_path = "models/pdfTestUNI.pdf"  # Substitua pelo caminho do seu PDF
    extracted_text = pdf_to_text(pdf_path)
    xml_data = text_to_xml(extracted_text)

    with open("output.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("Conversão concluída! O arquivo XML foi salvo como output.xml.")
