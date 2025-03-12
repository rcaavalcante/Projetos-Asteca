import xmltodict
import os

lista_razao_cliente = []
lista_nat_op = []
lista_fornecedores = []
lista_nfs_alvo = []
lista_nfs_lidas = []

# Função para ler todos os arquivos XML em uma pasta e armazenar seu conteúdo
def ler_xmls_na_pasta(caminho_pasta):
    # Lista para armazenar os conteúdos dos arquivos XML
    lista_razao_cliente = []
    lista_nat_op = []
    
    # Percorre todos os arquivos na pasta
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        
        # Verifica se o arquivo é um arquivo XML
        if nome_arquivo.endswith('.xml'):
            with open(caminho_arquivo, "rb") as arquivo_alvo:
                # Converte o XML para dicionário
                dict_xml = xmltodict.parse(arquivo_alvo)
                
                # Acessando os valores 'natOp' e 'xNome' corretamente

                nat_operacao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['natOp']
                numero_nota = dict_xml['nfeProc']['NFe']['infNFe']['ide']['cNF']
                modelo = dict_xml['nfeProc']['NFe']['infNFe']['ide']['mod']
                #data_saida = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhSaiEnt']
                data_emissao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                tipo_nf = dict_xml['nfeProc']['NFe']['infNFe']['ide']['tpNF']

                if 'DEVOLU' or 'Devol' in nat_operacao:
                    preco_produto = dict_xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vProd']
                else:
                    preco_produto = None

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

                '''numero_fat = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['nFat']
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

                duplicatas_dict = {}

                for id, dup in enumerate(numero_duplicatas):
                    nDup = dup['nDup']
                    dVenc = dup['dVenc']
                    vDup = dup['vDup']

                    # Adicionando a duplicata ao dicionário
                    duplicatas_dict[f"duplicata_{nDup}"] = {
                        "nDup": nDup,
                        "dVenc": dVenc,
                        "vDup": vDup
                    }

                
                pagamentos = dict_xml['nfeProc']['NFe']['infNFe']['pag']['detPag']

                if isinstance(pagamentos, dict):
                    pagamentos = [pagamentos]

                pagamentos_dict = {}

                for idx, det_pag in enumerate(pagamentos):
                    #indPag = det_pag['indPag']
                    tPag = det_pag['tPag']
                    vPag = det_pag['vPag']
    
                # Adicionando o pagamento ao dicionário
                pagamentos_dict[f"pagamento_{str(idx+1).zfill(3)}"] = {
                    #"indPag": indPag,
                    "tPag": tPag,
                    "vPag": vPag
                }

                
                if 'dPag' in dict_xml['nfeProc']['NFe']['infNFe']['pag']['detPag']:
                    data_pagamento = dict_xml['nfeProc']['NFe']['infNFe']['pag']['detPag']['dPag']
                else:
                    data_pagamento = None'''
                
                # Adiciona os valores às listas
                lista_razao_cliente.append(razao_cliente)

                if nat_operacao not in lista_nat_op:
                    lista_nat_op.append(nat_operacao)
                lista_fornecedores.append(razao_fornecedor)
                lista_nfs_lidas.append(numero_nota)

                if nat_operacao == 'VENDA DE PRODUCAO DE ESTABELECIMENTO':
                    lista_nfs_alvo.append(numero_nota)



    # Retorna as listas com os valores extraídos
    return preco_produto


# Caminho para a pasta onde os arquivos XML estão armazenados
caminho_pasta = '/Users/rafaellacavalcante/Asteca/Projeto_NF/Arquivos_entrada_teste'
caminho_teste = '/Users/rafaellacavalcante/Asteca/Projeto_NF/teste'

# Chama a função para ler todos os arquivos XML na pasta
#clientes_lidos, operacoes, fornecedores, lista_alvo = ler_xmls_na_pasta(caminho_pasta)

print(ler_xmls_na_pasta(caminho_teste))

# Exibe os conteúdos extraídos
#print(clientes_lidos)  # Esperado: ['SAO PAULO CARNES E DERIVADOS LTDA', 'SAO PAULO CARNES E DERIVADOS EIRELI']

# print(len(operacoes))

# for operacao in operacoes:
#     print(operacao) 

# for fornecedor in fornecedores:
#     print(fornecedor)

# for nf in lista_alvo:
#     print(nf)