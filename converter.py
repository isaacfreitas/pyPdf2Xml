import fitz  # PyMuPDF
import xml.etree.ElementTree as ET
import datetime

def pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def text_to_xml(text):
    root = ET.Element("Document")
    content = ET.SubElement(root, "Content")
    content.text = text
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def structure_text_to_tiss(text):
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
    
    # Adicionar campos de exemplo, você deve extrair os dados reais de `text`
    ET.SubElement(transacao, "ans:tipoTransacao").text = "DEMONSTRATIVO_ANALISE_CONTA"
    ET.SubElement(transacao, "ans:sequencialTransacao").text = "01984750812"
    ET.SubElement(transacao, "ans:dataRegistroTransacao").text = datetime.datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(transacao, "ans:horaRegistroTransacao").text = datetime.datetime.now().strftime("%H:%M:%S")
    
    origem = ET.SubElement(cabecalho, "ans:origem")
    ET.SubElement(origem, "ans:registroANS").text = "317144"  # Exemplo, ajuste conforme a extração

    destino = ET.SubElement(cabecalho, "ans:destino")
    prestador = ET.SubElement(destino, "ans:identificacaoPrestador")
    ET.SubElement(prestador, "ans:codigoPrestadorNaOperadora").text = "11005013"  # Exemplo, ajuste conforme a extração

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
    ET.SubElement(cabecalho_demonstrativo, "ans:dataEmissao").text = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Dados Prestador
    dados_prestador = ET.SubElement(demonstrativo, "ans:dadosPrestador")
    dados_contratado = ET.SubElement(dados_prestador, "ans:dadosContratado")
    ET.SubElement(dados_contratado, "ans:codigoPrestadorNaOperadora").text = "11005013"
    ET.SubElement(dados_prestador, "ans:CNES").text = "3047091"

    # Dados Conta
    dados_conta = ET.SubElement(demonstrativo, "ans:dadosConta")
    dados_protocolo = ET.SubElement(dados_conta, "ans:dadosProtocolo")
    ET.SubElement(dados_protocolo, "ans:numeroLotePrestador").text = "134486"
    ET.SubElement(dados_protocolo, "ans:numeroProtocolo").text = "232685528"
    ET.SubElement(dados_protocolo, "ans:dataProtocolo").text = "2024-08-12"
    ET.SubElement(dados_protocolo, "ans:situacaoProtocolo").text = "6"

    # Epilogo
    epilogo = ET.SubElement(root, "ans:epilogo")
    ET.SubElement(epilogo, "ans:hash").text = "69a376127eb4e7e5f11f4e1a8bca391e"

    return ET.tostring(root, encoding="ISO-8859-1", xml_declaration=True)

if __name__ == "__main__":
    pdf_path = "models/pdfTest.pdf"  # Substitua pelo caminho do seu PDF
    extracted_text = pdf_to_text(pdf_path)
    xml_data = structure_text_to_tiss(extracted_text)

    with open("output_tiss.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("Conversão concluída! O arquivo XML TISS foi salvo como output_tiss.xml.")
