from Pegando_contas import pegar_contas_parcelamentos
from constantes import diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples, diretorio_pgfn
import os
from contextlib import redirect_stdout

# Definição do arquivo que vai armazenar o último parcelamento
arquivo_parcelamento = "parcelamento.txt"

def obter_parcelamento(cliente_cnpj):
    with open(os.devnull, 'w') as fnull:
        with redirect_stdout(fnull):
            contas_por_cliente = pegar_contas_parcelamentos(diretorio_pgfn)
    
    # Tenta obter os parcelamentos para o CNPJ fornecido
    parcelamentos = contas_por_cliente.get(cliente_cnpj, [])
    
    # Se não houver parcelamentos, retorna uma lista vazia
    if not parcelamentos:
        return []

    # Se o arquivo parcelamento.txt existir, lê o último parcelamento processado
    if os.path.exists(arquivo_parcelamento):
        with open(arquivo_parcelamento, 'r') as file:
            ultimo_parcelamento = file.read().strip()
    else:
        ultimo_parcelamento = None

    # Encontra o próximo parcelamento a ser processado
    if ultimo_parcelamento:
        try:
            index_atual = parcelamentos.index(ultimo_parcelamento)
            proximo_parcelamento = parcelamentos[index_atual + 1] if index_atual + 1 < len(parcelamentos) else "NENHUM"
        except ValueError:
            proximo_parcelamento = parcelamentos[0]  # Se não encontrar o último, começa do primeiro
    else:
        proximo_parcelamento = parcelamentos[0]  # Se for a primeira execução, começa do primeiro

    # Salva o parcelamento atual no arquivo para a próxima execução
    with open(arquivo_parcelamento, 'w') as file:
        file.write(proximo_parcelamento)

    # Retorna o próximo parcelamento
    return proximo_parcelamento