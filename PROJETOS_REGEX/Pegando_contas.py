import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
import re
import pandas as pd

def pegar_contas_parcelamentos(diretorio):
    # Dicionário para armazenar as contas de cada cliente
    contas_por_cliente = {}

    # Loop para percorrer os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.pdf'):  # Verifica se o arquivo é um PDF
            caminho_pdf = os.path.join(diretorio, arquivo)
            
            # Pegando CNPJ do cliente
            partes = arquivo.split('_')
            cnpj_cliente = partes[1][:14]
            
            #print(f"------------------------CLIENTE_{cnpj_cliente}------------------------")

            contas_encontradas = []  # Inicializando a variável para cada arquivo

            # Lê o arquivo PDF
            with open(caminho_pdf, "rb") as relatorio_sitfis:
                leitor = PyPDF2.PdfReader(relatorio_sitfis)

                conteudo_sispar_simples = ""  # Variável para armazenar o conteúdo após a referência_parcelamentos[0]
                conteudo_sispar = ""  # Variável para armazenar o conteúdo após a referência_parcelamentos[1]
                referencia_encontrada = False  # Flag para indicar se a referência 0 foi encontrada
                texto_pagina = ""
                texto_pos_referencia = ""
                
                # Percorre as páginas do PDF
                for i, pagina in enumerate(leitor.pages):
                    texto_pagina += pagina.extract_text()

                    #print(texto_pagina)
                    
                    # Verifica se algum dos textos de referência está no texto da página
                    for texto in referencia_parcelamentos:
                        if texto in texto_pagina:
                            
                            # Condições específicas para cada tipo de texto encontrado
                            if texto == referencia_parcelamentos[0]: 
                                #print(f"Cliente: {cnpj_cliente} - {referencia_parcelamentos[0]}: encontrado na pagina {i+1}")
                                referencia_encontrada = True
                                posicao_referencia = texto_pagina.find(texto)

                            elif texto == referencia_parcelamentos[1]:
                                #print(f"Cliente: {cnpj_cliente} - {referencia_parcelamentos[1]}: encontrado na página {i+1}")
                                if not referencia_encontrada:
                                    referencia_encontrada = True
                                    posicao_referencia = texto_pagina.find(texto)

                        if referencia_encontrada:
                            texto_pos_referencia = texto_pagina[posicao_referencia:]
                            #print(texto_pos_referencia)
                            contas_encontradas = re.findall(r'\d{9}', texto_pos_referencia)  # Busca números com 9 dígitos consecutivos
                    
                    # Se encontrar contas em uma página, pode parar de buscar
                    if contas_encontradas:
                        break
                        
                # Verifica se foi encontrado algum número de conta
                if contas_encontradas:
                    contas_por_cliente[cnpj_cliente] = contas_encontradas
                    #print(f"\nContas encontradas para o CNPJ {cnpj_cliente}: {contas_encontradas}")
                else:
                    print(f"\nNenhuma conta encontrada para o CNPJ {cnpj_cliente}.")
                    print("--------------------------------------------------")

    # Imprime o resumo das contas encontradas
    
    print("\n===================================")
    print(f"Contas de {len(contas_por_cliente)} clientes")
    print("Resumo:")
    for cnpj, contas in contas_por_cliente.items():
        print(f"CNPJ {cnpj}: {contas}")
        print("===================================")

    return contas_por_cliente

# Bloco principal para execução direta do script
if __name__ == "__main__":
    contas = pegar_contas_parcelamentos(diretorio_main)
    #print(type(contas))

    df = pd.DataFrame(list(contas.items()), columns=['CNPJ', 'Contas'])

    # Agora, exportando esse DataFrame para um arquivo Excel
    df.to_excel('Parcelamentos_PGFN.xlsx', index=False) 

    print("Arquivo Excel 'Parcelamentos_PGFN.xlsx' gerado com sucesso!")