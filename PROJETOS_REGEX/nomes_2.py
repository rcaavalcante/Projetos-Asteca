from Pegando_contas import pegar_contas_parcelamentos
from constantes import diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples, diretorio_pgfn
import os
from contextlib import redirect_stdout


def obter_parcelamento(cliente_cnpj):
    with open(os.devnull, 'w') as fnull:
        with redirect_stdout(fnull):
            contas_por_cliente = pegar_contas_parcelamentos(diretorio_pgfn)
    
    # Verifica se o dicionário foi preenchido corretamente
    #print("Dicionário de contas por cliente:", contas_por_cliente)  # Diagnóstico

    # Tenta obter os parcelamentos para o CNPJ fornecido
    parcelamentos = contas_por_cliente.get(cliente_cnpj, [])
    print(parcelamentos)
    
    # Verifica se o parcelamento foi encontrado ou se está vazio
    if parcelamentos:
        return parcelamentos
    else:
        return []
        
# Bloco principal para execução direta do script
# if __name__ == "__main__":
#     obter_parcelamento('00075112000101')  # Testa com o CNPJ fornecido
