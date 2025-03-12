import xmltodict
import os
import itertools

# Função para ler todos os arquivos XML em uma pasta e armazenar seu conteúdo
def ler_xmls_na_pasta(caminho_pasta):
    arquivos_xml = []  # Lista para armazenar os conteúdos dos arquivos XML
    
    # Percorre todos os arquivos na pasta
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        
        # Verifica se o arquivo é um arquivo XML
        if nome_arquivo.endswith('.xml'):
            with open(caminho_arquivo, "rb") as arquivo_alvo:
                # Converte o XML para dicionário
                dict_xml = xmltodict.parse(arquivo_alvo)
                arquivos_xml.append(dict_xml)  # Armazena o dicionário na lista
    
    #print(type(dict_xml))
    return dict_xml



# Caminho para a pasta onde os arquivos XML estão armazenados
caminho_pasta = '/Users/rafaellacavalcante/Asteca/Projeto_NF/Arquivos_entrada_teste'  # Substitua pelo caminho correto
caminho_teste = '/Users/rafaellacavalcante/Asteca/Projeto_NF/teste'
#ler_xmls_na_pasta(caminho_teste)

# # Chama a função para ler todos os arquivos XML na pasta
conteudo_xmls = ler_xmls_na_pasta(caminho_teste)

# Exibe os conteúdos dos arquivos XML

print(conteudo_xmls)

nat_operacao = conteudo_xmls['nfeProc']['NFe']['infNFe']['ide']['natOp']
#print(nat_operacao)

# print("************************************************************************************************************************************************")
data_emissao = conteudo_xmls['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
print(data_emissao)

numero_nota = conteudo_xmls['nfeProc']['NFe']['infNFe']['ide']['cNF']
print(numero_nota)

razao_fornecedor = conteudo_xmls['nfeProc']['NFe']['infNFe']['emit']['xNome']
print(razao_fornecedor)

razao_cliente = conteudo_xmls['nfeProc']['NFe']['infNFe']['dest']['xNome']
print(razao_cliente)

valor_original = conteudo_xmls['nfeProc']['NFe']['infNFe']['cobr']['fat']['vOrig']
print(valor_original)

#valor_desconto = conteudo_xmls['nfeProc']['NFe']['infNFe']['cobr']['fat']['vDesc']
#print(valor_desconto)

valor_pago = conteudo_xmls['nfeProc']['NFe']['infNFe']['pag']['detPag']['vPag']
print(valor_pago)

#data_pagamento = conteudo_xmls['nfeProc']['NFe']['infNFe']['pag']['detPag']['dPag']
#print(data_pagamento)

