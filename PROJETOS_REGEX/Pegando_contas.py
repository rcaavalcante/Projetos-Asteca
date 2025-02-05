import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
import re



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

            
            # Lê o arquivo PDF
            with open(caminho_pdf, "rb") as relatorio_sitfis:
                leitor = PyPDF2.PdfReader(relatorio_sitfis)

                conteudo_sispar_simples = ""  # Variável para armazenar o conteúdo após a referência_parcelamentos[0]
                conteudo_sispar = ""  # Variável para armazenar o conteúdo após a referência_parcelamentos[1]
                referencia_encontrada = False  # Flag para indicar se a referência 0 foi encontrada
                contas_encontradas = ""
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
                    
                        else:
                            print(f"Erro na leirtura do arquivo: {arquivo}")

            
        if contas_encontradas:
            # Armazenar os números encontrados no dicionário
            contas_por_cliente[cnpj_cliente] = contas_encontradas
            #print(f"\nContas encontradas para o CNPJ {cnpj_cliente}: {contas_encontradas}")
        else:
            print(f"\nNenhuma conta encontrada para o CNPJ {cnpj_cliente}.")
            print("--------------------------------------------------")


    print("\n===================================")
    print(f"Contas de {len(contas_por_cliente)} clientes")
    print("Resumo:")
    for cnpj, contas in contas_por_cliente.items():
        print(f"CNPJ {cnpj}: {contas}")
        print("===================================")


                    

# Bloco principal para execução direta do script
if __name__ == "__main__":
    pegar_contas_parcelamentos(diretorio_sispar_pgfn)