import re
import pdfplumber
import pandas as pd

# Lê o arquivo PDF
with pdfplumber.open("Relatorio_Situação_Fiscal_RICARDO_PERUCHI.pdf") as arquivo:
    for i, pagina in enumerate(arquivo.pages):
        texto_pagina = pagina.extract_text()  # Extrai o texto da página
        print(f"Texto da Página {i + 1}:\n{texto_pagina}\n")

    # Inicializa as variáveis CNPJ, Razão Social e uma lista para pendências
    CNPJ = None
    razao_social = None
    parcelamentos = []
    receita_federal = "Diagnóstico Fiscal na Receita Federal"

    # Array de textos de referência
    textos_referencia = [
        "Diagnóstico Fiscal na Receita Federal e Procuradoria-Geral da Fazenda Nacional",
        "Diagnóstico Fiscal na Receita Federal",
        # "Diagnóstico Fiscal na Procuradoria - Geral da Fazenda Nacional",
        "CNPJ"
    ]

    # Percorre as páginas do PDF
    for i, pagina in enumerate(arquivo.pages):
        texto_pagina = pagina.extract_text()  # Extrai o texto da página

        if texto_pagina:  # Verifica se há texto na página
            encontrado = False  # Variável para rastrear se algum texto foi encontrado

            # Verifica se algum dos textos de referência está no texto da página
            for texto in textos_referencia:
                if texto in texto_pagina:
                    encontrado = True

                    # Condição para o primeiro texto específico
                    if texto == textos_referencia[0]:  # Se for o primeiro texto
                        situacao = "Não foram detectadas pendências/exigibilidades suspensas nos controles da Receita Federal e da Procuradoria-Geral da Fazenda Nacional."
                        pass

                    else:
                        # receita_federal = texto

                        if re.search(receita_federal, texto_pagina, re.IGNORECASE):
                            print("Achou")

                        # Busca por ocorrências da palavra "Parcelamento" e armazena em variáveis separadas
                        parcelamentos_encontrados = re.findall(r'Parcelamento.*?\)', texto_pagina, re.IGNORECASE)
                        print(parcelamentos_encontrados)

                        # Armazena as ocorrências de parcelamentos na lista
                        parcelamentos.extend(parcelamentos_encontrados)

    # Exibe as frases encontradas
    #print(parcelamentos)

     # Opcional: salvar os parcelamentos em um arquivo CSV
    # df = pd.DataFrame(parcelamentos, columns=['Frases com Parcelamento'])
    # df.to_csv("parcelamentos_encontrados.csv", index=False)


