import PyPDF2
import re

# Lê o arquivo PDF
with open("Relatorio Situação Fiscal ABRIGO COMENDADOR WALMOR LTDA -33637984000175-20241021.pdf", "rb") as arquivo:
    leitor = PyPDF2.PdfReader(arquivo)

    # Inicializa a variável CNPJ
    CNPJ = None

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
                    print(
                        "Não foram detectadas pendências/exigibilidades suspensas nos controles da Receita Federal e da Procuradoria-Geral da Fazenda Nacional."
                    )

                # Exemplo de extração de CNPJ
                cnpj_matches = re.findall(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto_pagina)
                if cnpj_matches:
                    for cnpj in cnpj_matches:
                        CNPJ = cnpj_matches[1]  # Armazena o primeiro CNPJ encontrado
# print(f"CNPJ encontrado na página {i + 1}: {cnpj}")

                break  # Para não continuar verificando outros textos

        if not encontrado:
            print(f"Nenhum dos textos de referência encontrado na página {i + 1}.")

print("O CNPJ do cliente alvo é:", CNPJ)