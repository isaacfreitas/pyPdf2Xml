import fitz  # PyMuPDF
import cv2
import numpy as np

def convert_pdf_to_images(pdf_path, dpi=200):
    """
    Converte as páginas do PDF em imagens.
    
    :param pdf_path: Caminho do arquivo PDF.
    :param dpi: Resolução das imagens.
    :return: Lista de imagens em formato numpy array.
    """
    images = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            pix = pdf[page_num].get_pixmap(dpi=dpi)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            images.append(img)
    return images

def detect_horizontal_lines(image, min_length=50, line_thickness=2):
    """
    Detecta linhas horizontais em uma imagem usando OpenCV.
    
    :param image: Imagem em formato numpy array.
    :param min_length: Comprimento mínimo das linhas detectadas.
    :param line_thickness: Tolerância para considerar uma linha como horizontal.
    :return: Lista de coordenadas das linhas horizontais detectadas.
    """
    # Converte para escala de cinza e aplica limiar
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Kernel para detectar linhas horizontais
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_length, line_thickness))
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Detecta contornos das linhas
    contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lines = [cv2.boundingRect(contour) for contour in contours]  # x, y, largura, altura

    return lines

# Exemplo de uso
if __name__ == "__main__":
    pdf_path = "models/PDF_TISS.pdf"  # Caminho do PDF
    images = convert_pdf_to_images(pdf_path)

    for page_num, image in enumerate(images, start=1):
        # Dimensões da página
        height, width = image.shape[:2]  # Altura = eixo Y, Largura = eixo X
        
        # Detectar linhas horizontais
        lines = detect_horizontal_lines(image)

        print(f"\nPágina {page_num}:")
        print(f"Dimensões máximas - Eixo X (largura): {width}, Eixo Y (altura): {height}")

        if lines:
            print("Linhas horizontais encontradas:")
            for line in lines:
                x, y, w, h = line
                print(f" - Coordenadas: x={x}, y={y}, largura={w}, altura={h}")
        else:
            print("Nenhuma linha horizontal encontrada.")
