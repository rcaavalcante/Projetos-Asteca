import os
import csv
import PyPDF2
import re

# Caminho para a pasta que contém os arquivos PDF
caminho_da_pasta = '/Users/rafaellacavalcante/Documentos/ASTECA'

# Caminho para o arquivo CSV de saída
caminho_csv = 'tabela_parcelamentos.csv'

# Criar e abrir o arquivo CSV para escrita
with open(caminho_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Escrever o cabeçalho do CSV
    writer.writerow(['CNPJ', 'Diagnóstico Fiscal na Receita Federal', 'Data'])

# Percorrendo todos os arquivos na pasta
for nome_arquivo in os.listdir(caminho_da_pasta):
    if nome_arquivo.endswith('.pdf'):
        caminho_pdf = os.path.join(caminho_da_pasta, nome_arquivo)

        # Abrindo e lendo o arquivo PDF
        with open(caminho_pdf, 'rb') as arquivo:
            leitor_pdf = PyPDF2.PdfReader(arquivo)
            conteudo = ''

            # Extraindo texto de cada página
            for pagina in leitor_pdf.pages:
                conteudo += pagina.extract_text() + '\n'

            # Extraindo informações específicas usando regex
            cnpj = re.search(r"CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", conteudo)

            # Se o título for encontrado, extrair
            cnpj_extraido = cnpj.group(1) if cnpj else 'N/A'

            # Escrevendo os dados no CSV
            writer.writerow([nome_arquivo, conteudo])

print(f'Dados extraídos e salvos em {caminho_csv}')