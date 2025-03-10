import PyPDF2
import os
from datetime import datetime
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_parc_pgfn, diretorio_sispar_pgfn_simples
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
                    
       
    return sorted(arquivos_PARCSN), sorted(arquivos_PERTSN), sorted(arquivos_PERSESN), sorted(arquivos_RELPSN)           

def salvar_todos_arquivos_parcelamentos(arquivos_PARCSN, arquivos_PERTSN, arquivos_PERSESN, arquivos_RELPSN, diretorio_destino):
    periodo = datetime.now().strftime('%Y%m')
    """
    Função para salvar os nomes de arquivos de várias listas de parcelamentos em um único arquivo de texto.

    Args:
    - arquivos_PARCSN (list): Lista de arquivos PARCSN.
    - arquivos_PERTSN (list): Lista de arquivos PERTSN.
    - arquivos_PERSESN (list): Lista de arquivos PERSESN.
    - arquivos_RELPSN (list): Lista de arquivos RELPSN.
    - diretorio_destino (str): O diretório onde o arquivo de texto será salvo.
    """
    # Certifique-se de que o diretório existe, caso contrário, crie
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Defina o nome do arquivo de texto
    arquivo_saida = os.path.join(diretorio_destino, f'todos_arquivos_parcelamentos_{periodo}.txt')

    # Abra o arquivo para escrita
    with open(arquivo_saida, 'w') as f:
        # Escreve todos os arquivos das listas no arquivo de texto
        f.write("Arquivos PARCSN:\n")
        for arquivo in arquivos_PARCSN:
            f.write(f"{arquivo}\n")

        f.write("\nArquivos PERTSN:\n")
        for arquivo in arquivos_PERTSN:
            f.write(f"{arquivo}\n")

        f.write("\nArquivos PERSESN:\n")
        for arquivo in arquivos_PERSESN:
            f.write(f"{arquivo}\n")

        f.write("\nArquivos RELPSN:\n")
        for arquivo in arquivos_RELPSN:
            f.write(f"{arquivo}\n")

    print(f"Arquivo de resultados criado em: {arquivo_saida}")


def salvar_listas_em_arquivos(listas, diretorio_destino):
    periodo = datetime.now().strftime('%Y%m')
    """
    Função para salvar várias listas de arquivos em arquivos de texto separados.

    Args:
    - listas (dict): Um dicionário onde as chaves são os nomes das listas
                     e os valores são as listas de arquivos.
    - diretorio_destino (str): O diretório onde os arquivos de texto serão salvos.
    """
    # Certifique-se de que o diretório existe, caso contrário, crie
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Itera sobre as listas e cria um arquivo para cada uma
    for lista_nome, lista_arquivos in listas.items():
        # Define o nome do arquivo baseado no nome da lista
        nome = f'{lista_nome}_{periodo}.txt'
        arquivo_saida = os.path.join(diretorio_destino, nome)

        # Abre o arquivo para escrita
        with open(arquivo_saida, 'w') as f:
            f.write(f"Arquivos {lista_nome}:\n")
            for arquivo in lista_arquivos:
                f.write(f"{arquivo}\n")

        print(f"Arquivo {nome} criado em: {arquivo_saida}")



# Conferindo a lista de arquivos 
if __name__ == "__main__":
    # Chama a função verificacao_parc_rf e desempacota o retorno em variáveis
    arquivos_PARCSN, arquivos_PERTSN, arquivos_PERSESN, arquivos_RELPSN = verificacao_parc_rf()

    # Define o caminho do diretório onde os arquivos de texto serão salvos
    diretorio_destino = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos'

    # Criando um dicionário com as listas a serem salvas
    listas = {
        'arquivos_PARCSN': arquivos_PARCSN,
        'arquivos_PERTSN': arquivos_PERTSN,
        'arquivos_PERSESN': arquivos_PERSESN,
        'arquivos_RELPSN': arquivos_RELPSN
    }

    # Chama a função para salvar as listas nos arquivos de texto
    salvar_listas_em_arquivos(listas, diretorio_destino)
    #salvar_todos_arquivos_parcelamentos(arquivos_PARCSN, arquivos_PERTSN, arquivos_PERSESN, arquivos_RELPSN, diretorio_destino)