import PyPDF2
import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
import re
import shutil


def processar_arquivos(diretorio):

    #arquivos_parcelamento_sispar_pgfn = []
    #arquivos_parcelamento_sispar_pgfn_simples = []
    arquivos_parcelamento_pgfn = []
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
                    

                    if "PGFN" in pendencias:
                        #parcelamento_encontrado = False

                        for texto in referencia_parcelamentos:
                            
                            if texto in texto_pagina:
                                if referencia_parcelamentos[0] in texto_pagina:
                                    #print(f"{referencia_parcelamentos[0]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #parcelamento_encontrado = True
                                    #arquivos_parcelamento_sispar_pgfn_simples.append(arquivo)
                                    arquivos_parcelamento_pgfn.append(arquivo)
                                    break

                                if referencia_parcelamentos[1] in texto_pagina:
                                    #print(f"{referencia_parcelamentos[1]} encontrado na página {i + 1} do relatório do cliente {cnpj_cliente}")
                                    #arquivos_parcelamento_sispar_pgfn.append(arquivo)
                                    #parcelamento_encontrado = True
                                    if arquivo not in arquivos_parcelamento_pgfn:
                                        arquivos_parcelamento_pgfn.append(arquivo) 

            except:
                print(f"Erro na leitura do arquivo: {arquivo}")

         
    if arquivos_parcelamento_pgfn:
        print("\n", diretorio, "\n")
        print(f"{arquivos_processados} arquivos processados")
        print(f"\n{len(arquivos_parcelamento_pgfn)} Arquivos com parcelamentos ativos na PGFN: ")
        for arquivo in arquivos_parcelamento_pgfn:
            print(f"- {arquivo}")


    else:
        print(f"Não foram encontrados arquivos com Parcelamentos SISPAR ativos na PGFN.")

    #return arquivos_parcelamento_pgfn





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
    processar_arquivos(diretorio_main)
    # arquivos_alvo = processar_arquivos(diretorio_main)
    # pasta_origem = os.path.join(diretorio_main)
    # pasta_destino = diretorio_sispar_pgfn
    #mover_arquivos_para_pasta(arquivos_alvo, pasta_origem, pasta_destino)


# Bloco principal para execução direta do script
# if __name__ == "__main__":
#     processar_arquivos(diretorio_main)