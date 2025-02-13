import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
import re
import shutil


def processar_arquivos(diretorio):

    #arquivos_parcelamento_sispar_pgfn = []
    #arquivos_parcelamento_sispar_pgfn_simples = []
    arquivos_parcelamento_geral = []
    arquivos_processados = 0
    parc_receita = ["PERT", "PERSE", "RELP"]


    for arquivo in os.listdir(diretorio):
        tem_parc_receita = False
        if arquivo.endswith('.pdf'):  # Verifica se o arquivo é um PDF
            arquivos_processados += 1
            caminho_pdf = os.path.join(diretorio, arquivo)
                
            # Pegando CNPJ do cliente
            partes = arquivo.split('_')
            cnpj_cliente = partes[1][:14]
                
            #print(f"------------------------CLIENTE_{cnpj_cliente}------------------------")

            pendencias = []

            try:     
                # Lê o arquivo PDF
                with open(caminho_pdf, "rb") as relatorio_sitfis:
                    leitor = PyPDF2.PdfReader(relatorio_sitfis)
                        
                    texto_pagina = ""

                    # Percorre as páginas do PDF
                    for i, pagina in enumerate(leitor.pages):
                        texto_pagina += pagina.extract_text()
                            
                            
                            
                    #print(texto_pagina)

                            
                    # Verifica se algum dos textos de referência está no texto da página
                    for texto in referencia_pendencias:
                        if texto in texto_pagina:    
                        # Condições específicas para cada tipo de texto encontrado
                            if texto == referencia_pendencias[0]: 
                                pendencias.append("Não foram detectadas pendências/exigibilidades suspensas nos controles da Receita Federal e da Procuradoria-Geral da Fazenda Nacional.")
                                break  # Se encontrar esse texto, não há pendências
                                    
                            elif texto == referencia_pendencias[1]:  # Se for o segundo texto
                                pendencias.append("Receita Federal")
                                    
                            elif texto == referencia_pendencias[2]:  # Se for o terceiro texto
                                sem_pendencia = "Não foram detectadas pendências/exigibilidades suspensas para esse contribuinte nos controles da Procuradoria-Geral da Fazenda Nacional."
                                if sem_pendencia in texto_pagina:
                                    pendencias.append("Sem pendências na PGFN")
                                else: 
                                    pendencias.append("PGFN")

                    # Após percorrer todas as páginas, verificamos as pendências
                    if pendencias:
                        pass
                        #print(f"Pendências cliente {cnpj_cliente}: {pendencias}")
                    else:
                        print(f"Erro ao ler o pdf: {arquivo}") 

                    #print(texto_pagina)
                    

                    if "PGFN" in pendencias:
                        #parcelamento_encontrado = False

                        for texto in referencia_parcelamentos:
                            
                            if texto in texto_pagina:
                                if referencia_parcelamentos[0] in texto_pagina:
                                    #print(f"{referencia_parcelamentos[0]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #parcelamento_encontrado = True
                                    #arquivos_parcelamento_sispar_pgfn_simples.append(arquivo)
                                    arquivos_parcelamento_geral.append(arquivo)
                                    break

                                if referencia_parcelamentos[1] in texto_pagina:
                                    #print(f"{referencia_parcelamentos[1]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #arquivos_parcelamento_sispar_pgfn.append(arquivo)
                                    #parcelamento_encontrado = True
                                    if arquivo not in arquivos_parcelamento_geral:
                                        arquivos_parcelamento_geral.append(arquivo) 

                    elif "Receita Federal" in pendencias:

                        for parc in parc_receita:
                            if parc in texto_pagina:
                                tem_parc_receita = True
                            
                                if parc_receita[0] in texto_pagina:
                                    print(f"{parc_receita[0]} está no SITFIS do cliente: {cnpj_cliente}")

                                if parc_receita[1] in texto_pagina:
                                    print(f"{parc_receita[1]} está no SITFIS do cliente: {cnpj_cliente}")

                                if parc_receita[2] in texto_pagina:
                                    print(f"{parc_receita[2]} está no SITFIS do cliente: {cnpj_cliente}")

                    if tem_parc_receita:
                        pass
                        #print(f"O cliente {cnpj_cliente} tem parcelamentos PERT, PERSE ou RELP")
                    

            except:
                print(f"Erro na leitura do arquivo: {arquivo}")


# Conferindo a lista de arquivos 
if __name__ == "__main__":
    processar_arquivos(diretorio_main)
    

