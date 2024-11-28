import fitz  # PyMuPDF
import xml.etree.ElementTree as ET


def find_nearby_words(pdf_path, target_x, target_y, tolerance):
    """
    Encontra e retorna as palavras próximas às coordenadas especificadas (target_x, target_y)
    dentro de uma área de tolerância, concatenando-as em uma única string.
    
    :param pdf_path: Caminho do arquivo PDF.
    :param target_x: Coordenada x do ponto alvo.
    :param target_y: Coordenada y do ponto alvo.
    :param tolerance: Tolerância para considerar blocos próximos do alvo.
    :return: String com as palavras encontradas na área próxima.
    """
    words_found = []
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            words = page.get_text("words")  # Extrai cada palavra com coordenadas
            for word in words:
                x0, y0, x1, y1, text = word[:5]
                if (x0 - tolerance<= target_x <= x1 + tolerance and 
                    y0 <= target_y <= y1 ):
                    print(f"Texto encontrado na página {page_num}:\n{text}\n")
                    words_found.append(text)
    return " ".join(words_found) if words_found else "Texto não encontrado"

def find_horizontal_lines(pdf_path, tolerance=2):
    """
    Identifica linhas horizontais consecutivas em cada página do PDF.
    
    :param pdf_path: Caminho do arquivo PDF.
    :param tolerance: Tolerância para considerar linhas consecutivas (em pixels).
    :return: Lista de coordenadas das linhas horizontais consecutivas para cada página.
    """
    line_pairs = []  # Lista para armazenar pares de linhas consecutivas

    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            # Obtém todos os objetos gráficos da página
            shapes = page.get_drawings()

            # Filtra apenas as linhas horizontais
            horizontal_lines = []
            for shape in shapes:
                for item in shape["items"]:
                    if item[0] == "l":  # O objeto é uma linha
                        x0, y0, x1, y1 = item[1:5]
                        if abs(y0 - y1) <= tolerance:  # Verifica se é horizontal
                            horizontal_lines.append((x0, y0, x1, y1))

            # Ordena as linhas por suas coordenadas verticais
            horizontal_lines.sort(key=lambda line: line[1])

            # Verifica pares consecutivos de linhas horizontais
            for i in range(len(horizontal_lines) - 1):
                _, y0, _, _ = horizontal_lines[i]
                _, y1, _, _ = horizontal_lines[i + 1]

                # Se a diferença vertical entre duas linhas consecutivas for menor que a tolerância, é um par
                if abs(y1 - y0) <= tolerance:
                    line_pairs.append((page_num, horizontal_lines[i], horizontal_lines[i + 1]))

    return line_pairs

# Função para construir o XML no padrão TISS com dados manuais para inicializar
def structure_text_to_tiss():
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
    ET.SubElement(transacao, "ans:sequencialTransacao").text = "01984750812"
    ET.SubElement(transacao, "ans:dataRegistroTransacao").text = "2024-10-10"
    ET.SubElement(transacao, "ans:horaRegistroTransacao").text = "09:00:03"
    
    origem = ET.SubElement(cabecalho, "ans:origem")
    ET.SubElement(origem, "ans:registroANS").text = "317144"
    
    destino = ET.SubElement(cabecalho, "ans:destino")
    prestador = ET.SubElement(destino, "ans:identificacaoPrestador")
    ET.SubElement(prestador, "ans:codigoPrestadorNaOperadora").text = "11005013"
    ET.SubElement(cabecalho, "ans:Padrao").text = "4.01.00"
    
    # Operadora para Prestador
    operadora_para_prestador = ET.SubElement(root, "ans:operadoraParaPrestador")
    demonstrativos_retorno = ET.SubElement(operadora_para_prestador, "ans:demonstrativosRetorno")
    demonstrativo = ET.SubElement(demonstrativos_retorno, "ans:demonstrativoAnaliseConta")
    
    cabecalho_demonstrativo = ET.SubElement(demonstrativo, "ans:cabecalhoDemonstrativo")
    ET.SubElement(cabecalho_demonstrativo, "ans:registroANS").text = "317144"
    ET.SubElement(cabecalho_demonstrativo, "ans:numeroDemonstrativo").text = "8928565"
    ET.SubElement(cabecalho_demonstrativo, "ans:nomeOperadora").text = "UNIMED FORTALEZA"
    ET.SubElement(cabecalho_demonstrativo, "ans:numeroCNPJ").text = "05868278000107"
    ET.SubElement(cabecalho_demonstrativo, "ans:dataEmissao").text = "2024-10-10"
    
    # Dados do Prestador
    dados_prestador = ET.SubElement(demonstrativo, "ans:dadosPrestador")
    dados_contratado = ET.SubElement(dados_prestador, "ans:dadosContratado")
    ET.SubElement(dados_contratado, "ans:codigoPrestadorNaOperadora").text = "11005013"
    ET.SubElement(dados_prestador, "ans:CNES").text = "3047091"

    # Dados Conta e Protocolo
    dados_conta = ET.SubElement(demonstrativo, "ans:dadosConta")
    dados_protocolo = ET.SubElement(dados_conta, "ans:dadosProtocolo")
    ET.SubElement(dados_protocolo, "ans:numeroLotePrestador").text = "134486"
    ET.SubElement(dados_protocolo, "ans:numeroProtocolo").text = "232685528"
    ET.SubElement(dados_protocolo, "ans:dataProtocolo").text = "2024-08-12"
    ET.SubElement(dados_protocolo, "ans:situacaoProtocolo").text = "6"

    # Estrutura das Guias e detalhes da guia (sem valores)
    relacao_guias = ET.SubElement(dados_protocolo, "ans:relacaoGuias")
    guia1 = ET.SubElement(relacao_guias, "ans:numeroGuiaPrestador").text = "3567286"
    guia2 = ET.SubElement(relacao_guias, "ans:numeroGuiaOperadora").text = "178849958"
    ET.SubElement(relacao_guias, "ans:numeroCarteira").text = "00630020068382626"
    ET.SubElement(relacao_guias, "ans:dataInicioFat").text = "2024-08-12"
    ET.SubElement(relacao_guias, "ans:horaInicioFat").text = "10:13:16"
    ET.SubElement(relacao_guias, "ans:situacaoGuia").text = "6"

    # Detalhes das guias sem preenchimento de valores, conforme instruções
    for _ in range(8):  # Número de vezes ajustável conforme necessário
        detalhes_guia = ET.SubElement(relacao_guias, "ans:detalhesGuia")
        ET.SubElement(detalhes_guia, "ans:sequencialItem")
        ET.SubElement(detalhes_guia, "ans:dataRealizacao")
        procedimento = ET.SubElement(detalhes_guia, "ans:procedimento")
        ET.SubElement(procedimento, "ans:codigoTabela")
        ET.SubElement(procedimento, "ans:codigoProcedimento")
        ET.SubElement(procedimento, "ans:descricaoProcedimento")
        ET.SubElement(detalhes_guia, "ans:valorInformado")
        ET.SubElement(detalhes_guia, "ans:qtdExecutada")
        ET.SubElement(detalhes_guia, "ans:valorProcessado")
        ET.SubElement(detalhes_guia, "ans:valorLiberado")
        ET.SubElement(detalhes_guia, "ans:relacaoGlosa")

    # Valores dos protocolos
    ET.SubElement(relacao_guias, "ans:valorInformadoGuia")
    ET.SubElement(relacao_guias, "ans:valorProcessadoGuia")
    ET.SubElement(relacao_guias, "ans:valorLiberadoGuia")
    ET.SubElement(relacao_guias, "ans:valorGlosaGuia")

    # Totalizadores
    ET.SubElement(dados_protocolo, "ans:valorInformadoProtocolo")
    ET.SubElement(dados_protocolo, "ans:valorProcessadoProtocolo")
    ET.SubElement(dados_protocolo, "ans:valorLiberadoProtocolo")
    ET.SubElement(dados_protocolo, "ans:valorGlosaProtocolo")

    ET.SubElement(demonstrativo, "ans:valorInformadoGeral")
    ET.SubElement(demonstrativo, "ans:valorProcessadoGeral")
    ET.SubElement(demonstrativo, "ans:valorLiberadoGeral")
    ET.SubElement(demonstrativo, "ans:valorGlosaGeral")

    # Epílogo
    epilogo = ET.SubElement(root, "ans:epilogo")
    ET.SubElement(epilogo, "ans:hash").text = "69a376127eb4e7e5f11f4e1a8bca391e"
    
    return ET.tostring(root, encoding="ISO-8859-1", xml_declaration=True)

# Executa e gera o arquivo XML com a estrutura definida
if __name__ == "__main__":
    pdf_path = "models/PDF_TISS.pdf"  # Caminho do PDF
    
    # Exemplo de uso da função de coordenadas com tolerância
    nearby_words1 = find_nearby_words(pdf_path, target_x=100, target_y=50, tolerance=0)
    nearby_words2 = find_nearby_words(pdf_path, target_x=200, target_y=50, tolerance=0)
    nearby_words3 = find_nearby_words(pdf_path, target_x=300, target_y=50, tolerance=0)
    print(f"Palavras próximas encontradas: {nearby_words1}")
    print(f"Palavras próximas encontradas: {nearby_words2}")
    print(f"Palavras próximas encontradas: {nearby_words3}")

    # Construindo o XML com a estrutura definida
    xml_data = structure_text_to_tiss()

    with open("output_tiss.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("\nConversão concluída! O arquivo XML TISS foi salvo como output_tiss.xml.\n")