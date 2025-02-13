import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
import re
import shutil
from Verificacao_pendencias_RF import processar_arquivos


def verificacao_parc_rf():

    lista_arquivos = processar_arquivos(diretorio_main)
    #print(len(lista_arquivos))
    # for i in sorted(lista_arquivos):
    #     print(i)  
    arquivos_processados = 0
    parc_receita = ["PERT", "PERSE", "RELP", "SIMPLES NACIONAL - EM PARCELAMENTO"]
    arquivos_PARCSN = []
    arquivos_PERTSN = []
    arquivos_RELPSN = []
    arquivos_PERSESN = []
    contador = 0


    for arquivo in lista_arquivos:
        tem_parc_receita = False
        if arquivo.endswith('.pdf'):  # Verifica se o arquivo é um PDF
            arquivos_processados += 1
            caminho_pdf = os.path.join(diretorio_main, arquivo)
                
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
                    

                    if "Receita Federal" in pendencias:

                        parcelamentos_identificados = [] 
                        
                        for parc in parc_receita:
                            if parc in texto_pagina:
                                tem_parc_receita = True
                                parcelamentos_identificados.append(parc)

                        for parc in parcelamentos_identificados:
                            if parc == "PERT":
                                arquivos_PERTSN.append(arquivo)
                                #print(f"{parc_receita[0]} está no SITFIS do cliente: {cnpj_cliente}")

                            elif parc == "PERSE":
                                arquivos_PERSESN.append(arquivo)
                                #print(f"{parc_receita[1]} está no SITFIS do cliente: {cnpj_cliente}")

                            elif parc == "RELP":
                                arquivos_RELPSN.append(arquivo)
                                #print(f"{parc_receita[2]} está no SITFIS do cliente: {cnpj_cliente}")
                                
                            elif parc == "SIMPLES NACIONAL - EM PARCELAMENTO":
                                arquivos_PARCSN.append(arquivo)
                                #print(f"PARCSN está no SITFIS do cliente: {cnpj_cliente}")
                                
                    

            except:
                print(f"Erro na leitura do arquivo: {arquivo}")

    
    if tem_parc_receita:
         #pass
        if arquivos_RELPSN:
            print(f"{len(arquivos_RELPSN)} arquivos com RELPSN:")
            for i in sorted(arquivos_RELPSN):
                print(i)
        else:
            print("**** Não há arquivos com parcelamento do tipo RELPSN ****")

        if arquivos_PERSESN:
            print(f"{len(arquivos_PERSESN)} arquivos com PERSESN:")
            for i in sorted(arquivos_PERSESN):
                print(i)
        else:
            print("**** Não há arquivos com parcelamento do tipo PERSESN ****")

        if arquivos_PERTSN:
            print(f"{len(arquivos_PERTSN)} arquivos com PERTSN:")
            for i in sorted(arquivos_PERTSN):
                print(i)
        else:
            print("**** Não há arquivos com parcelamento do tipo PERTSN ****")

        if arquivos_PARCSN:
            print(f"{len(arquivos_PARCSN)} arquivos com PARCSN:")
            for i in sorted(arquivos_PARCSN):
                print(i)
                                
        else:
            print("**** Não há arquivos com parcelamento do tipo PARCSN ****")
                    
       
                       







    '''
    print(f"{arquivos_processados} arquivos processados")
    print(f"{len(somente_PARCSN)} arquivos que possuem somente PARCSN: ")
    for i in sorted(somente_PARCSN):
        print(i)'''


# Conferindo a lista de arquivos 
if __name__ == "__main__":
    verificacao_parc_rf()
    
    

