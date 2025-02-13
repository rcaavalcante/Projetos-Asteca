import os
from constantes import diretorio_main, diretorio_teste, referencia_pendencias, referencia_parcelamentos, diretorio_pgfn, diretorio_sispar_pgfn, diretorio_sispar_pgfn_simples


def converter_cnpj(cnpj):
    """Converte o CNPJ removendo caracteres especiais."""
    return ''.join([c for c in cnpj if c.isdigit()])

def formatar_cnpjs(cnpjs):
    """Converte e ordena a lista de CNPJs."""
    # Converte e coloca aspas em volta
    #cnpjs_convertidos = ['"' + converter_cnpj(cnpj) + '"' for cnpj in cnpjs]
    cnpjs_convertidos = [converter_cnpj(cnpj) for cnpj in cnpjs]
    # Ordena a lista em ordem crescente
    cnpjs_convertidos.sort()
    return cnpjs_convertidos

# Exemplo de lista de CNPJs
contador = 0
cnpjs = ['04.956.309/0001-00',
            '43.940.515/0001-84',
            '17.910.909/0001-80',
            '39.818.429/0001-26',
            '01.682.442/0001-28',
            '09.404.882/0001-25',
            '33.262.015/0001-87',
            '37.794.160/0001-60',
            '57.864.754/0001-07',
            '15.343.435/0001-06',
            '51.747.386/0001-30',
            '30.449.282/0001-70',
            '20.276.958/0001-17',
            '20.769.676/0001-51',
            '54.479.694/0001-10',
            '97.545.949/0001-09',
            '26.920.835/0001-53',
            '22.336.007/0001-11',
            '27.732.407/0001-60',
            '47.079.965/0001-85',
            #'258.156.868-24',
            '03.356.754/0001-77',
            '54.264.657/0001-95',
            '39.682.413/0001-39',
            '17.219.586/0001-82',
            '11.145.516/0001-40',
            '00.597.582/0001-35',
            '08.139.911/0001-06',
            '49.231.794/0001-93',
            '04.455.308/0003-44',
            '06.341.035/0001-70',
            '37.167.362/0001-81',
            '07.069.527/0001-11',
            '20.373.154/0001-36',
            #'052.996.751-00',
            '57.723.469/0001-76',
            '45.619.362/0001-01',
            '10.139.647/0001-52',
            '09.400.550/0001-72',
            '02.374.034/0001-71',
            '10.759.594/0001-72',
            '10.829.906/0001-77',
            '59.478.198/0005-90',
            '46.503.012/0001-30',
            '75.222.901/0036-57',
            '57.615.441/0001-15',
            '45.037.229/0001-39',
            '32.944.766/0001-10',
            '18.309.699/0001-31',
            '56.193.953/0001-78',
            '01.479.626/0001-95',
            '01.739.861/0001-59',
            '04.918.941/0001-60',
            '02.321.770/0001-61',
            '06.299.272/0001-10',
            '47.676.876/0001-16',
            '30.821.927/0001-53',
            '02.715.000/0001-01',
            '56.480.235/0001-82',
            '46.262.674/0001-65',
            '47.646.012/0001-51',
            '43.020.321/0001-60',
            '43.214.851/0001-40',
            '31.385.027/0001-73',
            '54.399.127/0001-54',
            '46.953.166/0001-23',
            '25.024.092/0001-70',
            '05.764.194/0001-15',
            '08.865.892/0001-03',
            '05.195.537/0001-78',
            '55.436.655/0001-07',
            '21.340.293/0003-98',
            '06.219.783/0001-85',
            '24.185.633/0001-80',
            '01.496.359/0007-50',
            '07.916.671/0001-46',
            '15.735.291/0001-33',
            '34.778.620/0001-78',
            '47.807.337/0001-79',
            '50.394.171/0001-10',
            '24.865.643/0001-66',
            '32.429.411/0001-93',
            '12.525.292/0001-65',
            '00.075.112/0001-01',
            '55.480.173/0001-46',
            '25.141.771/0001-20',
            '31.839.487/0001-24',
            '09.615.457/0001-85',
            '52.074.987/0001-92',
            '47.986.571/0001-00',
            '02.494.299/0001-03',
            '37.839.594/0001-39',
            '17.844.578/0001-27',
            '21.778.116/0001-26',
            '06.084.614/0017-42',
            '05.605.725/0001-27',
            '08.870.403/0001-01',
            '06.227.480/0001-04',
            '20.290.751/0003-69',
            '42.125.797/0001-01',
            '37.088.659/0001-51',
            '02.541.065/0001-70',
            '10.556.232/0001-84',
            '51.995.820/0001-00'
]

    # Chama a função para converter e ordenar
cnpjs_formatados = formatar_cnpjs(cnpjs)

# Exibe o resultado
for cnpj in cnpjs_formatados:
    contador += 1 
    
print(f"Numero de clientes: {contador}")
#print(f"Numero de clientes: {contador}.\nCNPJs:\n" + "\n".join(cnpjs_formatados))
#print(cnpjs_formatados)


def arquivos_clientes(diretorio):

    arquivos_nao_encontrados = []
    arquivos_processados = 0
    cnpj_arquivos_gerados = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.pdf'):  # Verifica se o arquivo é um PDF
            arquivos_processados += 1
            caminho_pdf = os.path.join(diretorio, arquivo)
                
            # Pegando CNPJ do cliente
            partes = arquivo.split('_')
            cnpj_cliente = partes[1][:14]
            cnpj_arquivos_gerados.append(cnpj_cliente)
                
            #print(f"------------------------CLIENTE_{cnpj_cliente}------------------------")

    #print(len(cnpj_arquivos_gerados))

    
    for i in cnpjs_formatados:
        #print(i)
        if i in cnpj_arquivos_gerados:
            pass
        else:
            arquivos_nao_encontrados.append(i)
            #print(f"Arquivo NÃO encontrado para o CNPJ {i}")


    # Verifica quais CNPJs não tiveram arquivos correspondentes
    if arquivos_nao_encontrados:
        print(f"\n{len(arquivos_nao_encontrados)} CNPJs sem arquivos correspondentes:")
        for cnpj in arquivos_nao_encontrados:
            print(cnpj)
    else:
        print("\nTodos os arquivos foram encontrados para os CNPJs da lista!")



if __name__ == "__main__":
     arquivos_clientes(diretorio_main)

