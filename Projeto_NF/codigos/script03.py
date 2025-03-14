import xmltodict
import os
import pandas as pd

# Função para ler todos os arquivos XML em uma pasta e armazenar seu conteúdo
def ler_xmls_na_pasta(caminho_pasta):
    sucessos = 0
    # Lista para armazenar os conteúdos dos arquivos XML
    dados_tabela = []
    
    # Percorre todos os arquivos na pasta
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        
        # Verifica se o arquivo é um arquivo XML
        if nome_arquivo.endswith('.xml'):
            with open(caminho_arquivo, "rb") as arquivo_alvo:
                print("Arquivo: ", nome_arquivo)
                # Converte o XML para dicionário
                dict_xml = xmltodict.parse(arquivo_alvo)
                
                # Acessando os valores 'natOp' e 'xNome' corretamente
                nat_operacao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['natOp']
                numero_nota = dict_xml['nfeProc']['NFe']['infNFe']['ide']['cNF']
                modelo = dict_xml['nfeProc']['NFe']['infNFe']['ide']['mod']
                if 'dhSaiEnt' in dict_xml['nfeProc']['NFe']['infNFe']['ide']:
                    data_saida = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhSaiEnt']
                else: 
                    data_saida = None
                data_emissao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                tipo_nf = dict_xml['nfeProc']['NFe']['infNFe']['ide']['tpNF']

                # Preço do produto, se a operação for uma devolução
                if 'DEVOLU' in nat_operacao or 'Devol' in nat_operacao:
                    preco_produto = dict_xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vProd']
                else:
                    preco_produto = None

                # Acessando dados do fornecedor e do cliente dependendo do tipo de NF
                if tipo_nf == '1':      
                    razao_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['emit']['xNome']
                    cnpj_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['emit']['CNPJ']
                    razao_cliente = dict_xml['nfeProc']['NFe']['infNFe']['dest']['xNome']
                    cnpj_cliente = dict_xml['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
                elif tipo_nf == '0':
                    razao_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['dest']['xNome']
                    cnpj_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
                    razao_cliente =  dict_xml['nfeProc']['NFe']['infNFe']['emit']['xNome']
                    cnpj_cliente = dict_xml['nfeProc']['NFe']['infNFe']['emit']['CNPJ']


                if 'cobr' in dict_xml['nfeProc']['NFe']['infNFe']:
                    # Acessando dados da fatura
                    numero_fat = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['nFat']
                    valor_original = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vOrig']

                    if 'vDesc' in dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']:
                        valor_desconto = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vDesc']
                    else:
                        valor_desconto = None

                    valor_liquido = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vLiq']
                    numero_duplicatas = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['dup']

                    # Se numero_duplicatas for um dicionário, transformamos em uma lista
                    if isinstance(numero_duplicatas, dict):
                        numero_duplicatas = [numero_duplicatas]

                else:
                    # Caso 'cobr' não exista, todos os valores serão None
                    numero_fat = valor_original = valor_desconto = valor_liquido = numero_duplicatas = None

                # Criando dicionário de duplicatas
                duplicatas_dict = {}
                if numero_duplicatas:
                    for id, dup in enumerate(numero_duplicatas):
                        nDup = dup['nDup']
                        dVenc = dup['dVenc']
                        vDup = dup['vDup']
                        duplicatas_dict[f"duplicata_{nDup}"] = {
                            "nDup": nDup,
                            "dVenc": dVenc,
                            "vDup": vDup
                        }

                # Acessando dados de pagamentos
                pagamentos = dict_xml['nfeProc']['NFe']['infNFe']['pag']['detPag']
                if isinstance(pagamentos, dict):
                    pagamentos = [pagamentos]

                pagamentos_dict = {}
                for idx, det_pag in enumerate(pagamentos):
                    tPag = det_pag['tPag']
                    vPag = det_pag['vPag']
                    # Acessando a data de pagamento (dPag), se existir
                    if 'dPag' in det_pag:
                        data_pagamento = det_pag['dPag']
                    else:
                        data_pagamento = None

                    pagamentos_dict[f"pagamento_{str(idx+1).zfill(3)}"] = {
                        "tPag": tPag,
                        "vPag": vPag,
                        "dPag": data_pagamento
                        }

                # Montando a linha para a tabela
                linha = {
                    'Razao_Cliente': razao_cliente,
                    'CNPJ_Cliente': cnpj_cliente,
                    'Razao_Fornecedor': razao_fornecedor,
                    'CNPJ_Fornecedor': cnpj_fornecedor,
                    'Nat_Operacao': nat_operacao,
                    'Numero_NF': numero_nota,
                    'Modelo': modelo,
                    'Data_Saida': data_saida,
                    'Data_Emissao': data_emissao,
                    'Tipo_NF': tipo_nf,
                    'Numero_Fat': numero_fat,
                    'Valor_Original': valor_original,
                    'Valor_Desconto': valor_desconto,
                    'Valor_Liquido': valor_liquido,
                    'Preco_Produto': preco_produto,
                    'Duplicatas': duplicatas_dict,
                    'Pagamentos': pagamentos_dict
                }

                # Adicionando a linha ao conjunto de dados
                dados_tabela.append(linha) 
                
                #print(f"Arquivo {nome_arquivo} lido com sucesso!")
                sucessos += 1

    # Criando o DataFrame com os dados coletados
    df = pd.DataFrame(dados_tabela)

    # Retorna o DataFrame com as informações extraídas
    #return df
    return sucessos


# Caminho para a pasta onde os arquivos XML estão armazenados
caminho_pasta = '/Users/rafaellacavalcante/Asteca/Projeto_NF/Arquivos_entrada_teste'
caminho_teste = '/Users/rafaellacavalcante/Asteca/Projeto_NF/teste'

# Chamando a função para ler os XMLs e gerar a tabela
#data_frame = ler_xmls_na_pasta(caminho_pasta)
sucessos = ler_xmls_na_pasta(caminho_teste)
print(sucessos)

# Salvando o DataFrame em um arquivo CSV
#data_frame.to_csv('tabela_nfs_teste1.csv', index=False)
