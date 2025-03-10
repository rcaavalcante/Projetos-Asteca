import os
import json
from constantes_parcelamentos import diretorio_pert, diretorio_parc, diretorio_relp, diretorio_geral, arquivos_gerados 
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo


def parcelamentos_disponiveis(diretorio):
    lista_cnpjs = []
    tipos_parcelamentos = []
    atrasos = []

    # Percorrendo os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        # Verifica se o arquivo é um arquivo .json
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # Extraindo o cnpj 
            partes = arquivo.split('_')
            cnpj_cliente = partes[1]
            tipo_parcelamento = partes[0]
            
            # Abre o arquivo e carrega o conteúdo
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = json.load(f)

                qtde_parcelas = len(conteudo['listaParcelas'])
                parcelas_em_atraso = qtde_parcelas - 1

                #print(f'A quantidade de parcelas disponíveis do cliente {cnpj_cliente} é: {qtde_parcelas}')
                
                if tipo_parcelamento == 'PARCELASPARAGERAR162':
                    #print("*****PARCSN*****")
                    if parcelas_em_atraso == 0:    
                        pass    
                        #print(f"O cliente {cnpj_cliente} não possui parcelas em atraso")
                    else:
                        lista_cnpjs.append(cnpj_cliente)
                        tipos_parcelamentos.append('PARCSN')
                        atrasos.append(parcelas_em_atraso) 
                        #print(f"O cliente {cnpj_cliente} possui {parcelas_em_atraso} parcelas em atraso")
                elif tipo_parcelamento == 'PARCELASPARAGERAR182':
                    #print("*****PERTSN*****")
                    if parcelas_em_atraso == 0:     
                        pass   
                        #print(f"O cliente {cnpj_cliente} não possui parcelas em atraso")
                    else: 
                        lista_cnpjs.append(cnpj_cliente)
                        tipos_parcelamentos.append('PERTSN')
                        atrasos.append(parcelas_em_atraso) 
                        #print(f"O cliente {cnpj_cliente} possui {parcelas_em_atraso} parcelas em atraso")

                elif tipo_parcelamento == 'PARCELASPARAGERAR192':
                    #print("*****RELPSN*****")
                    if parcelas_em_atraso == 0: 
                        pass      
                        #print(f"O cliente {cnpj_cliente} não possui parcelas em atraso")
                    else: 
                        lista_cnpjs.append(cnpj_cliente)
                        tipos_parcelamentos.append('RELPSN')
                        atrasos.append(parcelas_em_atraso) 
                        #print(f"O cliente {cnpj_cliente} possui {parcelas_em_atraso} parcelas em atraso")

    # Agora, retornamos as listas após o loop percorrer todos os arquivos
    return lista_cnpjs, tipos_parcelamentos, atrasos



def gerar_tabela_excel_com_formato(lista_cnpjs, tipos_parcelamentos, atrasos, caminho_arquivo_excel):
    # Cria uma nova planilha do Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Parcelas em Atraso'

    # Adiciona o cabeçalho da tabela
    ws.append(['CNPJ', 'Tipo de Parcelamento', 'Parcelas em Atraso'])

    # Preenche as linhas com os dados das listas
    for cnpj, tipo, atraso in zip(lista_cnpjs, tipos_parcelamentos, atrasos):
        ws.append([cnpj, tipo, atraso])

    # Cria uma tabela no intervalo de dados
    tabela = Table(displayName="TabelaParcelas", ref=f"A1:C{len(lista_cnpjs)+1}")

    # Adiciona um estilo à tabela
    estilo_tabela = TableStyleInfo(
        name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=True
    )
    tabela.tableStyleInfo = estilo_tabela

    # Adiciona a tabela à planilha
    ws.add_table(tabela)

    # Salva a planilha em um arquivo Excel
    wb.save(caminho_arquivo_excel)
    print(f'Tabela salva em {caminho_arquivo_excel}')

# Exemplo de uso
lista_cnpjs = ['12345678000101', '98765432000198', '12398765432100']
tipos_parcelamentos = ['ParcelamentoSimples', 'ParcelamentoFacilitado', 'ParcelamentoAvançado']
atrasos = [3, 1, 2]

if __name__ == "__main__":
    #parcelamentos_disponiveis(diretorio_geral)
    lista_cnpjs, tipos_parcelamentos, atrasos = parcelamentos_disponiveis(diretorio_geral)
    #print(lista_cnpjs)

    gerar_tabela_excel_com_formato(lista_cnpjs, tipos_parcelamentos, atrasos, f"{arquivos_gerados}/Parcelas_atraso_teste.xlsx")
