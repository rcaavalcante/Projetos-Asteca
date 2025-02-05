import re
import json
import os
from datetime import datetime

# Caminho do arquivo JSON gerado pelo lerpdf.py
json_path = '/Users/rafaellacavalcante/PycharmProjects/pythonProject/Asteca/PROJETO1/biblioteca_textos.json'

# Verificar se o arquivo JSON existe
if not os.path.exists(json_path):
    print(f"Arquivo JSON {json_path} não encontrado.")
else:
    # Carregar o conteúdo do arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as json_file:
        biblioteca_textos = json.load(json_file)

    # Expressões regulares para cada campo
    regex_patterns = {
        "CNPJ": r"CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})",
        "UA de Domicílio": r"UA de Domicílio:\s*([^Código da UA]+)\s*Código da UA",
        "Código da UA": r"Código da UA:\s*([\d.]+)",
        "Endereço": r"Endereço:\s*([^Bairro]+)\s*Bairro",
        "Bairro": r"Bairro:\s*([^CEP]+)\s*CEP",
        "CEP": r"CEP:\s*(\d{5}-\d{3})",
        "Município": r"Município:\s*([A-Z\s]+)\s*UF",
        "UF": r"UF:\s*([A-Z]{2})",
        "Responsável": r"Responsável:\s*([\d.-]+\s*-\s*[A-Z\s]+)",
        "Situação": r"Situação:\s*([A-Z]+)",
        "Natureza Jurídica": r"Natureza Jurídica:\s*([\d-]+\s*-\s*[A-Z\s]+)\s*Data de Abertura",
        "Data de Abertura": r"Data de Abertura:\s*(\d{2}/\d{2}/\d{4})",
        "CNAE": r"CNAE:\s*([\d-]+/\d{2}\s*-\s*[A-Z\s,]+)\s*Porte da Empresa",
        "Porte da Empresa": r"Porte da Empresa:\s*([A-Z\s]+)"
    }

    # Iterar sobre os textos extraídos do JSON
    for arquivo_pdf, empresas in biblioteca_textos.items():
        print(f"Processando o arquivo: {arquivo_pdf}")
        print("=" * 80)

        for empresa_texto in empresas:
            # A variável 'texto' agora está associada ao conteúdo de cada empresa
            texto = empresa_texto

            # Dicionário para armazenar os resultados para esta empresa
            resultados = {}

            # Aplicar cada regex no texto da empresa
            for campo, regex in regex_patterns.items():
                match = re.search(regex, texto)
                if match:
                    valor = match.group(1).strip()
                    if campo == "Data de Abertura":
                        # Converter a Data de Abertura para datetime
                        try:
                            valor = datetime.strptime(valor, '%d/%m/%Y')
                        except ValueError:
                            valor = None  # Se a conversão falhar, definir como None
                    resultados[campo] = valor

            # Exibir os resultados extraídos para cada empresa
            print("Dados da Empresa:")
            print("-" * 40)
            for campo, valor in resultados.items():
                if campo == "Data de Abertura" and isinstance(valor, datetime):
                    valor_formatado = valor.strftime('%d/%m/%Y')
                    print(f"{campo}: {valor_formatado}")
                else:
                    print(f"{campo}: {valor}")
            print()  # Linha em branco para separar empresas
        print("=" * 80)

print(len(biblioteca_textos))