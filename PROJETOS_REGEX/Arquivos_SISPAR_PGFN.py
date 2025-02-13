import os
from PROJETOS_REGEX.Verificacao_pendencias_PGFN import processar_arquivos, arquivos_parcelamento_pgfn, diretorio_sispar_pgfn
from contextlib import redirect_stdout
import shutil
from constantes import diretorio_main, diretorio_teste, diretorio_sispar_pgfn, diretorio_pgfn

# Chama a função para processar os arquivos e preencher a lista mas sem exibir os prints da função
arquivos = processar_arquivos(diretorio_main)

def mover_arquivos_para_pasta(arquivos, pasta_origem, pasta_destino):
    # Contadores para sucesso e falha
    sucesso = 0
    falha = 0

    if arquivos == []:
        #print("Nenhum SITFIS com parcelamento SISPAR-PGFN foi encontrado ")
        return "Nenhum SITFIS com parcelamento SISPAR-PGFN foi encontrado"
    
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
    pasta_origem = os.path.join(diretorio_main)
    pasta_destino = diretorio_sispar_pgfn
    mover_arquivos_para_pasta(arquivos_parcelamento_pgfn, pasta_origem, pasta_destino)
