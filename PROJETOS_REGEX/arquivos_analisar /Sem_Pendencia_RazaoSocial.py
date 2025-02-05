import re
import PyPDF2
import pandas as pd

# Lê o arquivo PDF
with open("Relatorio Situação Fiscal 3F COMERCIO DE CARNES LTDA -43940515000184-20241021.pdf", "rb") as arquivo:
    leitor = PyPDF2.PdfReader(arquivo)

    # Inicializa as variáveis CNPJ e Razão Social
    CNPJ = None
    razao_social = None

    # Array de textos de referência
    textos_referencia = [
        "Diagnóstico Fiscal na Receita Federal e Procuradoria-Geral da Fazenda Nacional",
        "Diagnóstico Fiscal na Receita Federal",
        "Diagnóstico Fiscal na Procuradoria - Geral da Fazenda Nacional,"
        "CNPJ"
    ]

    # Percorre as páginas do PDF
    for i, pagina in enumerate(leitor.pages):
        texto_pagina = pagina.extract_text()
        encontrado = False  # Variável para rastrear se algum texto foi encontrado

        # Verifica se algum dos textos de referência está no texto da página
        for texto in textos_referencia:
            if texto in texto_pagina:
                encontrado = True

                # Condição para o segundo texto específico
                if texto == textos_referencia[0]:  # Se for o segundo texto
                    situacao = "Não foram detectadas pendências/exigibilidades suspensas nos controles da Receita Federal e da Procuradoria-Geral da Fazenda Nacional."

                # Captura o número no formato 12.345.678 e a razão social após esse número
                match = re.search(r'(\d{2}\.\d{3}\.\d{3})\s+(.*)', texto_pagina)
                if match:
                    CNPJ = match.group(1)  # Captura o CNPJ
                    razao_social = match.group(2)  # Captura a razão social

                # Verifica se os valores foram capturados
                if CNPJ and razao_social:
                    break  # Sai do loop se ambos os valores forem encontrados

        if not encontrado:
            print(f"Nenhum dos textos de referência encontrado na página {i + 1}.")

# Formata a string CNPJ e Razão Social
if CNPJ and razao_social:
    CNPJ = f"CNPJ: {CNPJ} {razao_social}"

dados = {
    "Situação": [situacao]
}

# Cria um DataFrame a partir do dicionário
df = pd.DataFrame(dados)


# Criar um ExcelWriter para inserir a linha mestre acima do cabeçalho
with pd.ExcelWriter("relatorio_3fCOMERCIO_RAZAOSOCIAL.xlsx", engine='openpyxl') as writer:
    # Escrever a linha mestre como a primeira linha
    df_mestre = pd.DataFrame([[CNPJ, '', '']])  # Ajuste conforme necessário
    df_mestre.to_excel(writer, index=False, header=False, startrow=0)

    # Escrever o DataFrame final abaixo da linha mestre
    df.to_excel(writer, index=False, header=True, startrow=1)


print("Tabela criada com sucesso!")