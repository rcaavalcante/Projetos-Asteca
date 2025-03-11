import re
from datetime import datetime

data_atual = datetime.now().strftime('%Y%m')

# Caminhos dos arquivos

caminho_arquivo_geral = f"/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/todos_arquivos_parcelamentos_{data_atual}.txt"
caminho_arquivo_parcsn = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PARCSN_{data_atual}.txt'
caminho_arquivo_pertsn = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PERTSN_{data_atual}.txt'
caminho_arquivo_persesn = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PERSESN_{data_atual}.txt'
caminho_arquivo_relpsn = f'/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_RELPSN_{data_atual}.txt'

# Listas para armazenar os CNPJs
arquivos_parcsn = []
arquivos_pertsn = []
arquivos_persesn = []
arquivos_relpsn = []

# Expressão regular para capturar o CNPJ (14 dígitos consecutivos)
regex_cnpj = r'\d{14}'

# Função para processar os arquivos e extrair CNPJs
def extraindo_cnpj(caminho_arquivo, lista_destino):
    with open(caminho_arquivo, 'r') as file:
        for linha in file:
            if 'Situação Fiscal' in linha:
                # Buscar o CNPJ na linha
                cnpj_encontrado = re.search(regex_cnpj, linha)
                if cnpj_encontrado:
                    # Adiciona o CNPJ encontrado à lista
                    lista_destino.append(cnpj_encontrado.group())

# Processar os arquivos
extraindo_cnpj(caminho_arquivo_parcsn, arquivos_parcsn)
extraindo_cnpj(caminho_arquivo_pertsn, arquivos_pertsn)
extraindo_cnpj(caminho_arquivo_persesn, arquivos_persesn)
extraindo_cnpj(caminho_arquivo_relpsn, arquivos_relpsn)

#print(len(arquivos_parcsn))


# Exibir os CNPJs encontrados um por um
print(f"{len(arquivos_parcsn)} CNPJs em PARCSN:")
for cnpj in arquivos_parcsn:
    print(f'"{cnpj}",')

print(f"\n{len(arquivos_pertsn)} CNPJs em PERTSN:")
for cnpj in arquivos_pertsn:
    print(f'"{cnpj}",')

print(f"\n{len(arquivos_persesn)} CNPJs em PERSESN:")
for cnpj in arquivos_persesn:
    print(f'"{cnpj}",')

print(f"\n{len(arquivos_relpsn)} CNPJs em RELPSN:")
for cnpj in arquivos_relpsn:
    print(f'"{cnpj}",')


