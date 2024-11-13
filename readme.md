# Projeto de Extração e Conversão de PDF para XML no Padrão TISS

## Visão Geral
Este projeto realiza a extração de informações específicas de um arquivo PDF, utilizando coordenadas para localizar e identificar blocos de conteúdo. Os dados extraídos são organizados e convertidos para o padrão de XML TISS, de acordo com os requisitos estabelecidos pela ANS (Agência Nacional de Saúde Suplementar).

## Funcionalidades

- **Extração Baseada em Coordenadas**: A partir das coordenadas fornecidas (X, Y), o script localiza blocos específicos no PDF e extrai o texto associado.
- **Identificação de Blocos de Conteúdo**: Utiliza espaçamento vertical e horizontal para determinar separadores de seções dentro do PDF, permitindo a localização de cabeçalhos e seções importantes.
- **Conversão para XML no Padrão TISS**: Os dados extraídos são estruturados no formato XML conforme o padrão TISS, incluindo cabeçalho e dados específicos de operadoras de saúde.

## Estrutura do Projeto

```plaintext
.
├── converter.py          # Script principal que realiza a extração e conversão de dados
├── README.md             # Documentação do projeto
├── models/PDF_TISS.pdf   # PDF de exemplo para extração e conversão
└── output_tiss.xml       # Saída XML gerada no padrão TISS

##Pré-Requisitos
Python 3.7+
Bibliotecas Necessárias:
PyMuPDF (fitz): Para manipulação e extração de texto do PDF.
xml.etree.ElementTree: Para criação e manipulação do XML.
Instale as dependências com:


##Dependencias
pip install pymupdf
##Uso
Extração de Dados Específicos:

A função find_text_by_coordinates é usada para localizar texto próximo de coordenadas específicas (X, Y) no PDF.
Ajuste os valores de target_x, target_y, e tolerance para localizar diferentes seções.
Construção do XML TISS:

Com os dados extraídos, a função structure_text_to_tiss organiza as informações e gera o arquivo XML no padrão TISS.
Exemplo de Uso
python
Copiar código
python converter.py
Este comando:

Extrai texto específico do PDF baseado em coordenadas.
Constrói o arquivo XML output_tiss.xml no formato padrão TISS.
Estrutura do Código
find_text_by_coordinates: Localiza texto com base em coordenadas específicas, retornando o texto encontrado próximo ao ponto (X, Y).
structure_text_to_tiss: Organiza o conteúdo extraído no formato XML TISS, incluindo tags de cabeçalho, operadora e prestador de saúde.
Contribuição
Sinta-se à vontade para contribuir com sugestões de melhorias, novos recursos ou otimizações de desempenho. Para maiores informações, entre em contato com o mantenedor do projeto.