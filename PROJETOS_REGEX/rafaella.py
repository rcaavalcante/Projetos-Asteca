import shutil
import os
from Verificacao_pendencias import processa_arquivos
from constantes import diretorio_main, diretorio_sispar_pgfn

def mover_arquivos(pasta_origem, pasta_destino):
    # Obter a lista de arquivos retornados pela função processa_arquivos
    arquivos = processa_arquivos()

    # Verificar se a lista de arquivos não está vazia
    if arquivos:
        for arquivo_nome in arquivos:
            # Construir o caminho completo do arquivo
            arquivo_origem = os.path.join(pasta_origem, arquivo_nome)
            arquivo_destino = os.path.join(pasta_destino, arquivo_nome)

            # Verificar se o arquivo existe na pasta de origem
            if os.path.exists(arquivo_origem):
                try:
                    # Verificar se o arquivo já existe na pasta destino
                    if not os.path.exists(arquivo_destino):
                        shutil.move(arquivo_origem, arquivo_destino)
                        print(f"Arquivo {arquivo_nome} movido com sucesso para {pasta_destino}")
                    else:
                        print(f"O arquivo {arquivo_nome} já existe na pasta destino: {pasta_destino}")
                except Exception as e:
                    print(f"Erro ao mover o arquivo {arquivo_nome}: {e}")
            else:
                print(f"O arquivo {arquivo_nome} não foi encontrado na pasta de origem.")
    else:
        print("Nenhum arquivo para mover.")

# Chamada da função para mover os arquivos
if __name__ == "__main__":
    pasta_origem = diretorio_main
    pasta_destino = diretorio_sispar_pgfn
    mover_arquivos(diretorio_main, diretorio_sispar_pgfn)
