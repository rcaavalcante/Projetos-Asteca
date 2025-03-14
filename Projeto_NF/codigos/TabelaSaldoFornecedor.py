import xmltodict
import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import plotly.graph_objects as go


def ler_xmls_na_pasta(caminho_principal):
    # Lista para armazenar os conteúdos dos arquivos XML
    erros = 0
    sucessos = 0
    dados_tabela = []
    arquivos_erro = []
    arquivos_evento = []
    arquivos_lidos = 0
    lista_clientes = ['ABM', 'SAO PAULO', 'Sao Paulo', 'FC SOUSA', 'CELIA', 'CANDIO E QUEIROZ']
    lista_strings = ['DEV', 'Dev', 'dev']
    
    for i, (pasta_raiz, subpastas, arquivos) in enumerate(os.walk(caminho_principal)): 
        if i > 0:
            for nome_arquivo in os.listdir(pasta_raiz):
                caminho_arquivo = os.path.join(pasta_raiz, nome_arquivo)
                
                # Verifica se o arquivo é um arquivo XML
                if nome_arquivo.endswith('.xml'):
                    arquivos_lidos += 1
                    with open(caminho_arquivo, "rb") as arquivo_alvo:
                        #print("Arquivo: ", nome_arquivo)
                        # Converte o XML para dicionário
                        dict_xml = xmltodict.parse(arquivo_alvo)
                        
                        if "EVENTO" not in nome_arquivo:
                            try:
                                # Acessando os valores 'natOp' e 'xNome' corretamente
                                ide = dict_xml['nfeProc']['NFe']['infNFe']['@Id'][3:]
                                nat_operacao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['natOp']
                                numero_nota = dict_xml['nfeProc']['NFe']['infNFe']['ide']['cNF']
                                modelo = dict_xml['nfeProc']['NFe']['infNFe']['ide']['mod']
                                if 'dhSaiEnt' in dict_xml['nfeProc']['NFe']['infNFe']['ide']:
                                    data_saida = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhSaiEnt']
                                else: 
                                    data_saida = None
                                data_emissao = dict_xml['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                                tipo_nf = dict_xml['nfeProc']['NFe']['infNFe']['ide']['tpNF']
                                valor_nf = float(dict_xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vNF'])
                                razao_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['emit']['xNome']
                                cnpj_fornecedor = dict_xml['nfeProc']['NFe']['infNFe']['emit']['CNPJ']
                                razao_cliente = dict_xml['nfeProc']['NFe']['infNFe']['dest']['xNome']
                                cnpj_cliente = dict_xml['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
                                
                                # Preço do produto, se a operação for uma devolução
                                if any(item in nat_operacao for item in lista_strings):
                                    preco_produto = dict_xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vProd']
                                    valor_nf = float(dict_xml['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vNF']) - float(preco_produto)
                                else:
                                    if tipo_nf == '0' and any(cliente in razao_cliente for cliente in lista_clientes[1:3]):
                                        valor_nf = 0
                                    preco_produto = None
                                    

                                if 'cobr' in dict_xml['nfeProc']['NFe']['infNFe']:
                                    # Acessando dados da fatura
                                    numero_fat = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['nFat']
                                    valor_original = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vOrig']

                                    if 'vDesc' in dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']:
                                        valor_desconto = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vDesc']
                                    else:
                                        valor_desconto = None

                                    valor_liquido = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['fat']['vLiq']
                                    
                                    if 'dup' in dict_xml['nfeProc']['NFe']['infNFe']['cobr']:
                                        numero_duplicatas = dict_xml['nfeProc']['NFe']['infNFe']['cobr']['dup']
                                    else: 
                                        numero_duplicatas = None 

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
                                    'Valor da Nota': valor_nf,
                                    'Valor_Original': valor_original,
                                    'Valor_Desconto': valor_desconto,
                                    'Valor_Liquido': valor_liquido,
                                    'Preco_Produto': preco_produto,
                                    'Duplicatas': duplicatas_dict,
                                    'Pagamentos': pagamentos_dict,
                                    'ID': ide
                                }

                                # Adicionando a linha ao conjunto de dados
                                dados_tabela.append(linha) 
                                
                                #print(f"Arquivo {nome_arquivo} lido com sucesso!")
                                sucessos += 1
                            
                            except:
                                #print(f"Erro no arquivo {nome_arquivo}.")
                                erros += 1 
                                arquivos_erro.append(nome_arquivo)

                        elif "EVENTO" in nome_arquivo:
                            arquivos_evento.append(nome_arquivo)
                                

    # Criando o DataFrame com os dados coletados
    df_erro = pd.DataFrame(arquivos_erro, columns=["Nome_Arquivo"])
    df = pd.DataFrame(dados_tabela)

    # Agrupar por fornecedor e somar os valores das notas fiscais
    df_grouped_total = df.groupby('Razao_Fornecedor')['Valor da Nota'].sum().reset_index()
    df_grouped_total.rename(columns={'Valor da Nota': 'Total_Valor_Nota'}, inplace=True)

    # Adicionando a coluna de total por fornecedor ao DataFrame original
    df = pd.merge(df, df_grouped_total, on='Razao_Fornecedor', how='left')

    # Removendo duplicações para que cada fornecedor tenha apenas uma linha com o total
    df_unique = df.drop_duplicates(subset=['Razao_Fornecedor'])

    # Retorna o DataFrame com as informações extraídas
    return df_unique, erros, sucessos, df_erro, arquivos_evento, arquivos_lidos, arquivos_erro


pasta_geral = 'Z:/Rafaella/Notas_Fiscais/SaoPaulo2024'
# Chamando a função para ler os XMLs e gerar a tabela
#data_frame = ler_xmls_na_pasta(caminho_pasta_0124)
df_sucessos, erros, sucessos, df_erro, arquivos_evento, arquivos_lidos, arquivos_erro = ler_xmls_na_pasta(pasta_geral)

print(f"Sucessos: {sucessos}")
print(f"Erros: {erros}")
#print(f"Evento: {len(arquivos_evento)}")
#print(f'Arquivos lidos: {arquivos_lidos}')
arquivos_referencia = arquivos_lidos - len(arquivos_evento)
print(f'Referência:', arquivos_referencia)

# for arquivo in arquivos_erro:
#     print(arquivo)


def criando_ajustando_arquivo(df):
    # Salvando o DataFrame em um arquivo Excel
    file_name = 'Tabela_teste_unica.xlsx'
    df.to_excel(file_name, index=False, engine='openpyxl')

    # Carregar o arquivo Excel recém-criado
    wb = load_workbook(file_name)
    ws = wb.active  # Trabalha na aba ativa (primeira aba)

    # Ajustar a largura das colunas automaticamente
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Obtém a letra da coluna

        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)  # Encontra o maior tamanho de conteúdo na coluna
            except:
                pass

        adjusted_width = (max_length + 2)  # Ajusta a largura das colunas para não cobrir o conteúdo
        ws.column_dimensions[column].width = adjusted_width

    # Salvar o arquivo com o ajuste da largura das colunas, sobrescrevendo o original
    wb.save(file_name)
    
    return print(f'{file_name} criada e ajustada com sucesso.')

criando_ajustando_arquivo(df_sucessos)



def listando_arquivos(arquivos):
    for arquivo in arquivos:
        print(arquivo)


def criando_grafico_erro(arquivos):
    df_erro = pd.DataFrame(arquivos, columns=["Nome_Arquivo"])
    # Criando a figura
    fig, ax = plt.subplots(figsize=(4, 8))  # Tamanho do gráfico

    # Escondendo os eixos para mostrar apenas a tabela
    ax.axis('tight')
    ax.axis('off')

    # Plotando a tabela no gráfico
    ax.table(cellText=df_erro.values, colLabels=df_erro.columns, cellLoc='center', loc='center')

    # Exibindo o gráfico
    return plt.show()

def criando_grafico_sucessos(df):
    # Criando a figura
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=df.columns,  # Cabeçalhos da tabela
        fill_color='paleturquoise',  # Cor de fundo do cabeçalho
        align='center',  # Alinhamento do texto no cabeçalho
        font=dict(size=14, family="Arial, sans-serif", color='black')  # Tamanho da fonte no cabeçalho
    ),
    cells=dict(
        values=[df[col] for col in df.columns],  # Dados de cada coluna
        fill_color='lavender',  # Cor de fundo das células
        align='center',  # Alinhamento do texto nas células
        font=dict(size=12, family="Arial, sans-serif", color='black'),  # Tamanho da fonte nas células
        height=30  # Altura das células
    )
    )])

    # Ajustando o layout da tabela (título, tamanho e outras personalizações)
    fig.update_layout(
        title='Minha Tabela de Dados',
        height=600,  # Tamanho total da figura (altura da tabela)
        width=7000  # Tamanho total da figura (largura da tabela)
    )
    # Exibindo o gráfico
    return fig.show()

#criando_grafico_sucessos(df_sucessos)
