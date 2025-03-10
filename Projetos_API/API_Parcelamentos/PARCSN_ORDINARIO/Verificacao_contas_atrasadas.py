import re

# Caminhos dos arquivos
caminho_arquivo_parcsn = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PARCSN_202502.txt'
caminho_arquivo_pertsn = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PERTSN_202502.txt'
caminho_arquivo_persesn = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_PERSESN_202502.txt'
caminho_arquivo_relpsn = '/Users/rafaellacavalcante/Asteca/Projetos_API/API_Parcelamentos/Files/arquivos_parcelamentos/arquivos_RELPSN_202502.txt'

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

'''
# Exibir os CNPJs encontrados um por um
print("CNPJs em PARCSN:")
for cnpj in arquivos_parcsn:
    print(cnpj)

print("\nCNPJs em PERTSN:")
for cnpj in arquivos_pertsn:
    print(cnpj)

print("\nCNPJs em PERSESN:")
for cnpj in arquivos_persesn:
    print(cnpj)

print("\nCNPJs em RELPSN:")
for cnpj in arquivos_relpsn:
    print(cnpj)'''


