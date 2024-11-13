import fitz  # PyMuPDF

def get_pdf_page_dimensions(pdf_path):
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            rect = page.rect  # Retângulo da página com largura e altura
            print(f"Página {page_num}: Largura = {rect.width}, Altura = {rect.height}")

# Exemplo de uso
pdf_path = "models/PDF_TISS.pdf"  # Substitua pelo caminho do seu PDF
get_pdf_page_dimensions(pdf_path)
