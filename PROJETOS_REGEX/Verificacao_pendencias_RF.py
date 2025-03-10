import PyPDF2
import os
from constantes import diretorio_main, referencia_pendencias, referencia_parcelamentos_rf, referencia_parcelamentos, diretorio_pgfn, diretorio_parc_pgfn, diretorio_sispar_pgfn_simples
import re
import shutil


def processar_arquivos(diretorio):

    #arquivos_parcelamento_sispar_pgfn = []
    #arquivos_parcelamento_sispar_pgfn_simples = []
    arquivos_parcelamento_rf = []
    arquivos_processados = 0

    for arquivo in os.listdir(diretorio):
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
                    

                    if "Receita Federal" in pendencias:
                        #parcelamento_encontrado = False

                        for texto in referencia_parcelamentos_rf:
                            
                            if texto in texto_pagina:
                                if referencia_parcelamentos_rf[0] in texto_pagina:
                                    #print(f"{referencia_parcelamentos_rf[0]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #parcelamento_encontrado = True
                                    #arquivos_parcelamento_sispar_pgfn_simples.append(arquivo)
                                    arquivos_parcelamento_rf.append(arquivo)
                                    break

                                if referencia_parcelamentos_rf[1] in texto_pagina:
                                    #print(f"{referencia_parcelamentos_rf[1]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #arquivos_parcelamento_sispar_pgfn.append(arquivo)
                                    #parcelamento_encontrado = True
                                    if arquivo not in arquivos_parcelamento_rf:
                                        arquivos_parcelamento_rf.append(arquivo) 

            except:
                print(f"Erro na leitura do arquivo: {arquivo}")

       
    if arquivos_parcelamento_rf:
        print("\n", diretorio, "\n")
        print(f"{arquivos_processados} arquivos processados")
        arquivos_parcelamento_rf_ordenados = sorted(arquivos_parcelamento_rf)
        print(f"\n{len(arquivos_parcelamento_rf)} Arquivos com parcelamentos ativos na RF: ")
        for arquivo in arquivos_parcelamento_rf_ordenados:
            print(f"- {arquivo}")


    else:
        print(f"Não foram encontrados arquivos com Parcelamentos SISPAR ativos na PGFN.")

    return arquivos_parcelamento_rf





def mover_arquivos_para_pasta(arquivos, pasta_origem, pasta_destino):
    # Contadores para sucesso e falha
    sucesso = 0
    falha = 0

    if arquivos == []:
        print("Nenhum SITFIS com parcelamento SISPAR-PGFN foi encontrado ")
        #return "Nenhum SITFIS com parcelamento SISPAR-PGFN foi encontrado"
    
    else: 
        # Cria a pasta de destino se ela não existir
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        # Move os arquivos para a pasta de destino
        for arquivo in arquivos:
            caminho_origem = os.path.join(pasta_origem, arquivo)
            caminho_destino = os.path.join(pasta_destino, arquivo)
            
            try:
                # Move o arquivo
                shutil.move(caminho_origem, caminho_destino)
                sucesso += 1  # Incrementa o contador de sucesso
                print(f"Arquivo {arquivo} movido para {pasta_destino}")
            except Exception as e:
                falha += 1  # Incrementa o contador de falha
                print(f"Erro ao mover o arquivo {arquivo}: {e}")
            print("-----------------------------------------------------------------")
        
        # Exibe o resumo
        return(print(f"\nResumo da movimentação dos arquivos:\nArquivos movidos com sucesso: {sucesso}\nArquivos que falharam: {falha}"))


# Conferindo a lista de arquivos 
if __name__ == "__main__":
    arquivos = processar_arquivos(diretorio_main)
    origem = diretorio_main
    destino = f"{diretorio_main}/pendecias_rf"
    mover_arquivos_para_pasta(arquivos, origem, destino)