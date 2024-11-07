import fitz  # PyMuPDF
import xml.etree.ElementTree as ET
import datetime

def pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    print(text)        
    return text
#===============================================================================================
def text_to_xml(text):
    root = ET.Element("Document")
    content = ET.SubElement(root, "Content")
    content.text = text
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)
#===============================================================================================
# Mapeando as palavras do 

#===============================================================================================
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
    
    # Apenas estrutura de tags, sem valores
    ET.SubElement(transacao, "ans:tipoTransacao")
    ET.SubElement(transacao, "ans:sequencialTransacao")
    ET.SubElement(transacao, "ans:dataRegistroTransacao")
    ET.SubElement(transacao, "ans:horaRegistroTransacao")
    
    origem = ET.SubElement(cabecalho, "ans:origem")
    ET.SubElement(origem, "ans:registroANS")

    destino = ET.SubElement(cabecalho, "ans:destino")
    prestador = ET.SubElement(destino, "ans:identificacaoPrestador")
    ET.SubElement(prestador, "ans:codigoPrestadorNaOperadora")

    ET.SubElement(cabecalho, "ans:Padrao")
    
    # Operadora para Prestador
    operadora_para_prestador = ET.SubElement(root, "ans:operadoraParaPrestador")
    demonstrativos_retorno = ET.SubElement(operadora_para_prestador, "ans:demonstrativosRetorno")
    demonstrativo = ET.SubElement(demonstrativos_retorno, "ans:demonstrativoAnaliseConta")

    cabecalho_demonstrativo = ET.SubElement(demonstrativo, "ans:cabecalhoDemonstrativo")
    ET.SubElement(cabecalho_demonstrativo, "ans:registroANS")
    ET.SubElement(cabecalho_demonstrativo, "ans:numeroDemonstrativo")
    ET.SubElement(cabecalho_demonstrativo, "ans:nomeOperadora")
    ET.SubElement(cabecalho_demonstrativo, "ans:numeroCNPJ")
    ET.SubElement(cabecalho_demonstrativo, "ans:dataEmissao")
    
    # Dados Prestador
    dados_prestador = ET.SubElement(demonstrativo, "ans:dadosPrestador")
    dados_contratado = ET.SubElement(dados_prestador, "ans:dadosContratado")
    ET.SubElement(dados_contratado, "ans:codigoPrestadorNaOperadora")
    ET.SubElement(dados_prestador, "ans:CNES")

    # Dados Conta
    dados_conta = ET.SubElement(demonstrativo, "ans:dadosConta")
    dados_protocolo = ET.SubElement(dados_conta, "ans:dadosProtocolo")
    ET.SubElement(dados_protocolo, "ans:numeroLotePrestador")
    ET.SubElement(dados_protocolo, "ans:numeroProtocolo")
    ET.SubElement(dados_protocolo, "ans:dataProtocolo")
    ET.SubElement(dados_protocolo, "ans:situacaoProtocolo")

    # Epilogo
    epilogo = ET.SubElement(root, "ans:epilogo")
    ET.SubElement(epilogo, "ans:hash")

    return ET.tostring(root, encoding="ISO-8859-1", xml_declaration=True)
#=====================================================================
if __name__ == "__main__":
    pdf_path = "models/pdfTest.pdf"  # Substitua pelo caminho do seu PDF
    extracted_text = pdf_to_text(pdf_path)
    xml_data = structure_text_to_tiss(extracted_text)

    with open("output_tiss.xml", "wb") as xml_file:
        xml_file.write(xml_data)

    print("\nConversão concluída! O arquivo XML TISS foi salvo como output_tiss.xml.")
    print("\n")
