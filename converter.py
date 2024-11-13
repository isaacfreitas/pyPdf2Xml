import fitz  # PyMuPDF
import xml.etree.ElementTree as ET
import datetime

def find_text_by_coordinates(pdf_path, target_x, target_y, tolerance=10):
    """
    Encontra e retorna o texto no PDF próximo às coordenadas especificadas (target_x, target_y).
    """
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            blocks = page.get_text("blocks")  # Extrai blocos com coordenadas
            
            for block in blocks:
                x0, y0, x1, y1, text = block[:5]
                
                # Verifica se o bloco está dentro da tolerância das coordenadas alvo
                if (abs(x0 - target_x)<= tolerance and abs(y0 - target_y) <= tolerance):
                    print(f"Texto encontrado na página {page_num}:\n{text}\n")
                    return text  # Retorna o primeiro texto encontrado próximo às coordenadas
    
    print("Texto não encontrado nas coordenadas especificadas.")
    return ""

# Função para estruturar o XML de acordo com o padrão TISS
def structure_text_to_tiss(registro_ans, cnpj, nome_operadora):
    namespaces = {
        "": "http://www.ans.gov.br/padroes/tiss/schemas",
        "ans": "http://www.ans.gov.br/padroes/tiss/schemas",
        "ns2": "http://www.w3.org/2000/09/xmldsig#"
    }
    
    root = ET.Element("ans:mensagemTISS", attrib={
        "xmlns": namespaces[""],
        "xmlns:ans": namespaces["ans"],
        "xmlns:ns2": namespaces["ns2"]
    })
    
    # Cabeçalho
    cabecalho = ET.SubElement(root, "ans:cabecalho")
    transacao = ET.SubElement(cabecalho, "ans:identificacaoTransacao")
    ET.SubElement(transacao, "ans:tipoTransacao").text = "DEMONSTRATIVO_ANALISE_CONTA"
    ET.SubElement(transacao, "ans:sequencialTransacao").text = "01984750812"  # Exemplo
    ET.SubElement(transacao, "ans:dataRegistroTransacao").text = datetime.datetime.now().strftime("%Y-%m-%d") #retirar
    ET.SubElement(transacao, "ans:horaRegistroTransacao").text = datetime.datetime.now().strftime("%H:%M:%S") #retirar
    
    origem = ET.SubElement(cabecalho, "ans:origem")
    ET.SubElement(origem, "ans:registroANS").text = registro_ans
    
    destino = ET.SubElement(cabecalho, "ans:destino")
    prestador = ET.SubElement(destino, "ans:identificacaoPrestador")
    ET.SubElement(prestador, "ans:codigoPrestadorNaOperadora").text = cnpj
    ET.SubElement(cabecalho, "ans:Padrao").text = "4.01.00"
    
    # Operadora para Prestador
    operadora_para_prestador = ET.SubElement(root, "ans:operadoraParaPrestador")
    demonstrativo = ET.SubElement(ET.SubElement(operadora_para_prestador, "ans:demonstrativosRetorno"), "ans:demonstrativoAnaliseConta")
    
    cabecalho_demonstrativo = ET.SubElement(demonstrativo, "ans:cabecalhoDemonstrativo")
    ET.SubElement(cabecalho_demonstrativo, "ans:registroANS").text = registro_ans
    ET.SubElement(cabecalho_demonstrativo, "ans:numeroCNPJ").text = cnpj
    ET.SubElement(cabecalho_demonstrativo, "ans:nomeOperadora").text = nome_operadora
    ET.SubElement(cabecalho_demonstrativo, "ans:dataEmissao").text = datetime.datetime.now().strftime("%Y-%m-%d")

    # Epílogo
    ET.SubElement(ET.SubElement(root, "ans:epilogo"), "ans:hash")
    
    return ET.tostring(root, encoding="ISO-8859-1", xml_declaration=True) 
    
    #=====================================================================

if __name__ == "__main__":
    pdf_path = "models/PDF_TISS.pdf"  # Caminho do PDF
    
    # Extraindo algumas informações específicas a partir das coordenadas
    registro_ans = find_text_by_coordinates  (pdf_path, target_x=200, target_y=100, tolerance=10) # Prestador
    cnpj = find_text_by_coordinates          (pdf_path, target_x=200, target_y=100, tolerance=10) # Coordenadas de exemplo
    nome_operadora = find_text_by_coordinates(pdf_path, target_x=200, target_y=100, tolerance=10) # Coordenadas de exemplo
    
    # Construindo o XML com os dados extraídos
    xml_data = structure_text_to_tiss(registro_ans, cnpj, nome_operadora)

    with open("output_tiss.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("\nConversão concluída! O arquivo XML TISS foi salvo como output_tiss.xml.\n")
