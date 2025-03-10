import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_parc_pgfn, diretorio_sispar_pgfn_simples
import re


def processar_arquivos(diretorio):

    arquivos_parcelamento_sispar_pgfn = []
    arquivos_parcelamento_sispar_pgfn_simples = []
    arquivos_parcelamento_geral = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.pdf'):  # Verifica se o arquivo é um PDF
            caminho_pdf = os.path.join(diretorio, arquivo)
                
            # Pegando CNPJ do cliente
            partes = arquivo.split('_')
            cnpj_cliente = partes[1][:14]
                
            #print(f"------------------------CLIENTE_{cnpj_cliente}------------------------")

            pendencias = []
                
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
                    print(f"Pendências cliente {cnpj_cliente}: {pendencias}")
                else:
                    print(f"Erro ao ler o pdf: {arquivo}") 

                #print(texto_pagina)
                

                if "PGFN" in pendencias:
                    posicao_referencia = ""
                    parcelamento_encontrado = False

                    for texto in referencia_parcelamentos:
                        
                        if texto in texto_pagina:
                            if referencia_parcelamentos[0] in texto_pagina:
                                print(f"{referencia_parcelamentos[0]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                parcelamento_encontrado = True
                                posicao_referencia = texto_pagina.find(texto)
                                arquivos_parcelamento_sispar_pgfn_simples.append(arquivo)
                                arquivos_parcelamento_geral.append(arquivo)
                                break

                            elif referencia_parcelamentos[1] in texto_pagina:
                                print(f"{referencia_parcelamentos[1]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                posicao_referencia = texto_pagina.find(texto)
                                arquivos_parcelamento_sispar_pgfn.append(arquivo)
                                parcelamento_encontrado = True
                                if arquivo not in arquivos_parcelamento_geral:
                                    arquivos_parcelamento_geral.append(arquivo) 


    if not parcelamento_encontrado:       
        print(f"Para o cliente {cnpj_cliente}, não foi encontrado Parcelamentos SISPAR na PGFN.")


    else:
                # Exibe os arquivos que possuem parcelamento SISPAR
        if arquivos_parcelamento_sispar_pgfn_simples:
            print(f"\n{len(arquivos_parcelamento_sispar_pgfn_simples)} Arquivos com {referencia_parcelamentos[0]} encontrados:")
            for arquivo in arquivos_parcelamento_sispar_pgfn_simples:
                print(f"- {arquivo}")  # Adicionando um hífen ou apenas o nome do arquivo em uma linha
        else:
            print(f"*********Nenhum arquivo com {referencia_parcelamentos[0]} foi encontrado.*********")


                       
        # Exibe os arquivos que possuem parcelamento SISPAR
        if arquivos_parcelamento_sispar_pgfn:
            print(f"\n{len(arquivos_parcelamento_sispar_pgfn)} Arquivos com {referencia_parcelamentos[1]} encontrados:")
            for arquivo in arquivos_parcelamento_sispar_pgfn:
                print(f"- {arquivo}")  # Adicionando um hífen ou apenas o nome do arquivo em uma linha
        else:
            print(f"*********Nenhum arquivo com {referencia_parcelamentos[1]} foi encontrado.*********")

            
        if arquivos_parcelamento_sispar_pgfn and arquivos_parcelamento_sispar_pgfn and arquivos_parcelamento_geral:
            print(f"\n{len(arquivos_parcelamento_geral)} Arquivos com parcelamentos ativos na PGFN: ")
            for arquivo in arquivos_parcelamento_geral:
                print(f"- {arquivo}")


# Bloco principal para execução direta do script
if __name__ == "__main__":
    processar_arquivos(diretorio_main)
            