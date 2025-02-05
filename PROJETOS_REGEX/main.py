import PyPDF2
import os
import shutil
import re
import os
from Verificacao_pendencias import  arquivos_parcelamento_sispar_pgfn, processar_arquivos, arquivos_parcelamento_geral, diretorio_gen1
from contextlib import redirect_stdout
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples
from Arquivos_SISPAR_PGFN import mover_arquivos_para_pasta
from Pegando_contas import pegar_contas_parcelamentos


if __name__ == "__main__":
#    diretorio_alvo = diretorio_pgfn
    processar_arquivos(diretorio_main)
    pasta_origem = os.path.join(diretorio_main)
    pasta_destino = os.path.join(diretorio_sispar_pgfn)
    mover_arquivos_para_pasta(arquivos_parcelamento_geral, pasta_origem, pasta_destino)
    pegar_contas_parcelamentos(diretorio_pgfn)
