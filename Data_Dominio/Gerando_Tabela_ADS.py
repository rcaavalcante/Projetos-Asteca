import pandas as pd

def gerando_arquivo(ads_list, codigos_list, contratos_list, tipo_contrato_list, nome_arquivo, nome_coluna_empresa, nome_coluna_codigo, nome_coluna_status, nome_coluna_tipo_contrato):
    # Criar um DataFrame com os dados
    dados = {
        nome_coluna_empresa: ads_list,
        nome_coluna_codigo: codigos_list,
        nome_coluna_status: contratos_list,
        nome_coluna_tipo_contrato: tipo_contrato_list
    }

    # Cria um DataFrame a partir do dicionário
    df = pd.DataFrame(dados)

    # Salva o DataFrame em um arquivo Excel
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')

    print(f"Arquivo Excel '{nome_arquivo}' gerado com sucesso!")

